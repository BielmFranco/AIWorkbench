"""Trusted invocation worker for the small local function fixtures, not an OS sandbox."""
import contextlib
import importlib.util
import json
import sys


class RefundFixture:
    def __init__(self, data):
        self.mode = data["mode"]
        self.calls = data["calls"]
        self.effects = data["effects"]

    def refund(self, key):
        self.calls.append(["refund", key])
        if self.mode == "denied":
            return "denied"
        if self.mode == "pending":
            return "pending"
        self.effects += 1
        raise TimeoutError("response lost")

    def lookup(self, key):
        self.calls.append(["lookup", key])
        return "issued" if self.effects else "pending"

    def serialize(self):
        return {"__refund_fixture__": True, "mode": self.mode, "calls": self.calls, "effects": self.effects}


def main():
    request = json.load(sys.stdin)
    args = [RefundFixture(value) if isinstance(value, dict) and value.get("__refund_fixture__") else value for value in request["args"]]
    result = None
    exception = None
    message = None
    # Preserve logs as stderr; the worker's stdout is a single structured result.
    with contextlib.redirect_stdout(sys.stderr):
        try:
            spec = importlib.util.spec_from_file_location("candidate_artifact", request["artifact"])
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
            result = getattr(module, request["function"])(*args)
        except Exception as exc:
            exception, message = type(exc).__name__, str(exc)
    result_type = "tuple" if isinstance(result, tuple) else "set" if isinstance(result, set) else type(result).__name__
    payload = list(result) if isinstance(result, (tuple, set)) else result
    response = {"result": payload, "result_type": result_type, "args_after": [v.serialize() if isinstance(v, RefundFixture) else v for v in args], "exception": exception, "message": message}
    json.dump(response, sys.stdout)


if __name__ == "__main__":
    main()
