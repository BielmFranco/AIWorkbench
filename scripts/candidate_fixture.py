"""Invoke fixture functions in a child, keeping candidate imports out of the grader."""
import json
import os
from pathlib import Path
import subprocess
import sys
from process_control import run_bounded


class Candidate:
    def __init__(self, path):
        self.path = Path(path).resolve()

    def __getattr__(self, function):
        def call(*args):
            encoded = []
            for arg in args:
                if hasattr(arg, "mode") and hasattr(arg, "calls") and hasattr(arg, "effects"):
                    encoded.append({"__refund_fixture__": True, "mode": arg.mode, "calls": arg.calls, "effects": arg.effects})
                else:
                    encoded.append(arg)
            request = {"artifact": str(self.path), "function": function, "args": encoded}
            environment = os.environ.copy()
            environment.pop("PYTHONOPTIMIZE", None)
            run = run_bounded([sys.executable, str(Path(__file__).with_name("fixture_worker.py"))], input=json.dumps(request), env=environment, timeout=5)
            if run.returncode:
                raise RuntimeError(f"Candidate worker failed: {run.stderr.strip()}")
            try:
                response = json.loads(run.stdout)
                if not isinstance(response, dict) or "result" not in response or "result_type" not in response or "args_after" not in response:
                    raise ValueError("Worker did not produce a complete invocation result")
            except ValueError as exc:
                raise RuntimeError("Candidate worker exited without an invocation result") from exc
            if response.get("exception"):
                if response["exception"] == "ValueError":
                    raise ValueError(response.get("message", ""))
                raise RuntimeError(response.get("message", response["exception"]))
            for original, after in zip(args, response["args_after"]):
                if isinstance(original, list):
                    original[:] = after
                elif isinstance(original, dict):
                    original.clear()
                    original.update(after)
                elif hasattr(original, "mode") and after.get("__refund_fixture__"):
                    original.calls = [tuple(item) for item in after["calls"]]
                    original.effects = after["effects"]
            value = response["result"]
            if response["result_type"] == "tuple":
                return tuple(value)
            if response["result_type"] == "set":
                return set(value)
            return value
        return call
