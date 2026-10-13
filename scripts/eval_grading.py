"""Deterministic artifact graders. Human rubrics remain pending until reviewed."""
import json
import os
from pathlib import Path
import subprocess
import sys

from jsonschema import Draft202012Validator
from process_control import run_bounded


def contained(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f"Path escapes its root: {relative}")
    return path


def read_pointer(data, pointer):
    if pointer == "":
        return data
    if not pointer.startswith("/"):
        raise ValueError("JSON pointer must begin with /")
    for part in pointer[1:].split("/"):
        key = part.replace("~1", "/").replace("~0", "~")
        data = data[int(key)] if isinstance(data, list) else data[key]
    return data


def validate_observation(observation):
    if not isinstance(observation, dict):
        return "Adapter observation must be a JSON object"
    if "capture_complete" in observation and not isinstance(observation["capture_complete"], bool):
        return "capture_complete must be a boolean"
    reads = observation.get("resource_reads", [])
    if not isinstance(reads, list):
        return "resource_reads must be an array"
    for item in reads:
        if not isinstance(item, dict) or item.get("kind") != "resource_read" or not isinstance(item.get("skill"), str) or not isinstance(item.get("trace_ref"), str) or not item["trace_ref"]:
            return "Resource reads require instrumented kind, skill and trace_ref"
    if observation.get("usage") is not None and not isinstance(observation["usage"], dict):
        return "usage must be an object or null"
    if observation.get("provider_turn_completed") is not None and not isinstance(observation["provider_turn_completed"], bool):
        return "provider_turn_completed must be a boolean or null"
    return None


def grade_assertion(assertion, output_dir: Path, repo: Path):
    result = {"id": assertion["id"], "passed": False, "evidence": ""}
    try:
        kind = assertion["kind"]
        artifact = contained(output_dir, assertion["artifact"])
        if kind == "python_test":
            test = contained(repo, assertion["test"])
            environment = os.environ.copy()
            environment.pop("PYTHONOPTIMIZE", None)
            environment["AIWORKBENCH_OUTPUT_DIR"] = str(output_dir.resolve())
            run = run_bounded([sys.executable, str(test)], env=environment, cwd=output_dir, timeout=30)
            evidence = (run.stdout + run.stderr).strip()
            result.update(passed=run.returncode == 0 and "PASS: observed task outcomes" in run.stdout, evidence=evidence or "Grader did not complete")
        else:
            data = json.loads(artifact.read_text(encoding="utf-8"))
            if kind == "json_schema":
                schema = json.loads(contained(repo, assertion["schema"]).read_text(encoding="utf-8"))
                errors = list(Draft202012Validator(schema).iter_errors(data))
                result.update(passed=not errors, evidence="valid artifact schema" if not errors else "; ".join(e.message for e in errors))
            elif kind == "json_value":
                actual = read_pointer(data, assertion["pointer"])
                expected = assertion["expected"]
                # JSON numbers allow equivalent int/float representations; bool is not a number here.
                numeric = isinstance(actual, (int, float)) and not isinstance(actual, bool) and isinstance(expected, (int, float)) and not isinstance(expected, bool)
                result.update(passed=(numeric or type(actual) is type(expected)) and actual == expected, evidence=f"{assertion['pointer']}: actual={actual!r}, expected={expected!r}")
            elif kind == "json_one_of":
                actual = read_pointer(data, assertion["pointer"])
                values = assertion["values"]
                result.update(passed=any(type(actual) is type(v) and actual == v for v in values), evidence=f"{assertion['pointer']}: actual={actual!r}, allowed={values!r}")
            else:
                raise ValueError("Unknown grader kind: " + kind)
    except (OSError, UnicodeError, ValueError, KeyError, IndexError, TypeError, subprocess.TimeoutExpired) as exc:
        result["evidence"] = str(exc)
    return result


def grade_case(case, output_dir: Path, repo: Path, observation=None):
    if case["mode"] == "routing":
        error = validate_observation(observation or {})
        if error:
            return {"status": "ungraded", "checks": [], "reason": error}
        evidence = (observation or {}).get("resource_reads", [])
        skills = sorted({item["skill"] for item in evidence if isinstance(item, dict) and item.get("trace_ref") and item.get("skill")})
        expected = case["expected_skill"]
        observed = (expected in skills) if expected else (case["skill_under_test"] in skills)
        passed = observed if expected else not observed
        # Absence is only observable when the adapter certifies complete capture.
        if not (observation or {}).get("capture_complete") and not (expected and observed):
            return {"status": "ungraded", "checks": [], "reason": "No complete tool-read trace; selection cannot be inferred from self-report."}
        return {"status": "passed" if passed else "failed", "checks": [{"id": "resource-selection", "passed": passed, "evidence": {"resource_reads": evidence, "expected_skill": expected}}], "human_review": []}
    checks = [grade_assertion(a, output_dir, repo) for a in case["assertions"]]
    manual = [{"id": r["id"], "status": "pending", "criterion": r["criterion"], "pass_anchor": r["pass_anchor"]} for r in case.get("human_rubric", [])]
    status = "failed" if any(not c["passed"] for c in checks) else "needs_review" if manual else "passed"
    return {"status": status, "checks": checks, "human_review": manual}
