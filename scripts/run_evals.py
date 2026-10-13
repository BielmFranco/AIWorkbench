#!/usr/bin/env python3
"""Validate specs by default; explicitly run bounded, isolated agent trials with an adapter."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import signal
import statistics
import shutil
import subprocess
import sys
import time

from eval_grading import contained, grade_case, validate_observation
from validate import check_cases
from process_control import run_bounded
import validate_metadata
import validate_structure

ROOT = Path(__file__).resolve().parents[1]


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_hash(folder):
    digest = hashlib.sha256()
    for path in sorted(folder.rglob("*")):
        if path.is_file():
            digest.update(path.relative_to(folder).as_posix().encode())
            digest.update(path.read_bytes())
    return digest.hexdigest()


def run_trial(root, suite, case, condition, trial, destination, adapter, timeout):
    if condition not in ("baseline", "candidate") or not isinstance(trial, int) or trial < 1:
        raise ValueError("Invalid trial condition or number")
    run_dir = contained(destination, f"{case['id']}/{condition}/{trial}")
    run_dir.mkdir(parents=True, exist_ok=False)
    workspace = run_dir / "workspace"
    output = workspace / "output"
    output.mkdir(parents=True)
    if case["mode"] == "outcome":
        shutil.copytree(contained(root, case["fixtures"]), workspace / "fixtures")
    if condition == "candidate":
        names = [suite["skill"]] if case["mode"] == "outcome" else [p.name for p in (root / "skills").iterdir() if (p / "SKILL.md").is_file()]
        for name in names:
            shutil.copytree(root / "skills" / name, workspace / ".agents/skills" / name)
    target_skill_hash = tree_hash(root / "skills" / suite["skill"])
    loaded_skill_hash = tree_hash(workspace / ".agents/skills" / suite["skill"]) if condition == "candidate" else None
    fixture_hash = tree_hash(workspace / "fixtures") if case["mode"] == "outcome" else None
    request = {
        "protocol_version": 1,
        "case_id": case["id"], "mode": case["mode"], "condition": condition,
        "prompt": case["prompt"], "workspace": str(workspace.resolve()),
        "output_dir": str(output.resolve()), "observation_path": str((run_dir / "observation.json").resolve()),
    }
    request_path = run_dir / "request.json"
    write_json(request_path, request)
    started = time.monotonic()
    with request_path.open("r", encoding="utf-8") as stdin, (run_dir / "stdout.log").open("w", encoding="utf-8") as stdout, (run_dir / "stderr.log").open("w", encoding="utf-8") as stderr:
        timed_out = False
        launch_error = None
        try:
            run = run_bounded(adapter["command"], stdin=stdin, stdout=stdout, stderr=stderr, cwd=root, timeout=timeout)
            code = run.returncode
        except subprocess.TimeoutExpired:
            code, timed_out = -1, True
        except OSError as exc:
            code, launch_error = -1, str(exc)
    observation = {}
    observation_error = "Adapter did not produce observation.json"
    observation_path = run_dir / "observation.json"
    if observation_path.exists():
        try:
            observation = json.loads(observation_path.read_text(encoding="utf-8"))
            observation_error = validate_observation(observation)
            if not observation_error and observation.get("adapter_kind") != adapter["kind"]:
                observation_error = "Adapter observation kind does not match its configuration"
            if observation_error:
                observation = {}
        except (ValueError, UnicodeError):
            observation = {}
            observation_error = "Adapter observation is not valid JSON"
    if code or timed_out:
        verdict = {"status": "failed", "checks": [], "reason": "Adapter timed out" if timed_out else launch_error or f"Adapter exit code {code}"}
    elif observation_error:
        verdict = {"status": "failed", "checks": [], "reason": observation_error}
    else:
        verdict = grade_case(case, output, root, observation)
    fixture_modified = case["mode"] == "outcome" and tree_hash(workspace / "fixtures") != fixture_hash
    if fixture_modified:
        verdict = {"status": "failed", "checks": [], "reason": "Fixed input fixtures were modified during execution"}
    result = {
        "case_id": case["id"], "mode": case["mode"], "condition": condition, "trial": trial,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "adapter_kind": adapter["kind"], "exit_code": code, "timed_out": timed_out,
        "usage": observation.get("usage"), "model": observation.get("model"),
        "provider_turn_completed": observation.get("provider_turn_completed"),
        "skill_sha256": loaded_skill_hash, "target_skill_sha256": target_skill_hash,
        "fixtures_sha256": fixture_hash, "fixture_modified": fixture_modified,
        "case_sha256": hashlib.sha256(json.dumps(case, sort_keys=True).encode()).hexdigest(),
        "verdict": verdict,
    }
    write_json(run_dir / "result.json", result)
    return result


def summarize(results):
    summary = {}
    for condition in ("baseline", "candidate"):
        group = [r for r in results if r["mode"] == "outcome" and r["condition"] == condition]
        if not group:
            continue
        times = [r["elapsed_seconds"] for r in group]
        machine_passes = sum(bool(r["verdict"].get("checks")) and all(c["passed"] for c in r["verdict"]["checks"]) for r in group)
        summary[condition] = {
            "executions": len(group), "machine_passes": machine_passes,
            "machine_pass_rate": machine_passes / len(group),
            "human_review_pending": sum(r["verdict"]["status"] == "needs_review" for r in group),
            "mean_elapsed_seconds": statistics.mean(times),
            "elapsed_stddev_seconds": statistics.stdev(times) if len(times) > 1 else None,
        }
    if "baseline" in summary and "candidate" in summary:
        summary["observed_machine_pass_rate_delta"] = summary["candidate"]["machine_pass_rate"] - summary["baseline"]["machine_pass_rate"]
    summary["interpretation"] = "Descriptive sample statistics only. Pending human scores, fixture leakage and uncontrolled environments must be resolved before a quality or efficacy claim."
    return summary


def trial_counts(results, kind):
    return {
        "agent_adapter_executions": len(results) if kind == "agent" else 0,
        "live_trials": sum(r.get("provider_turn_completed") is True for r in results) if kind == "agent" else 0,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--adapter", type=Path, help="JSON config: command argument list and kind (agent or simulation)")
    parser.add_argument("--skill", action="append", help="Select suites by name; repeat as needed")
    parser.add_argument("--case", action="append", help="Select case IDs; repeat as needed")
    parser.add_argument("--trials", type=int, default=1)
    parser.add_argument("--max-runs", type=int, default=8, help="Explicit bound on provider executions")
    parser.add_argument("--timeout", type=int, default=300, help="Seconds per adapter process tree")
    parser.add_argument("--output", type=Path, default=ROOT / "evals/runs")
    args = parser.parse_args()
    if min(args.trials, args.max_runs, args.timeout) <= 0:
        parser.error("Trial, run and timeout limits must be positive")
    errors = validate_structure.check() + validate_metadata.check()
    try:
        case_errors, count = check_cases()
        errors += case_errors
    except Exception as exc:
        errors.append("Case validation failed: " + str(exc))
        count = 0
    if errors:
        write_json(ROOT / "evals/reports/latest.json", {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "deterministic": {"status": "failed", "suites": len(list((ROOT / "evals/cases").glob("*.json"))), "cases": count, "output": "\n".join(errors)},
            "behavioral": {"status": "not_run", "mode": "specification", "cases": count, "live_trials": 0, "reason": "Validation failed; no agent was executed."},
        })
        print("\n".join(errors), file=sys.stderr)
        return 1
    suites = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((ROOT / "evals/cases").glob("*.json"))]
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "deterministic": {"status": "passed", "suites": len(suites), "cases": count, "output": f"OK: {count} validated case specifications"},
        "behavioral": {"status": "not_run", "mode": "specification", "cases": count, "live_trials": 0, "reason": "No adapter selected; no agent or behavioral outcome was executed."},
    }
    if not args.adapter:
        write_json(ROOT / "evals/reports/latest.json", report)
        print(json.dumps(report, indent=2))
        return 0
    adapter = json.loads(args.adapter.read_text(encoding="utf-8"))
    if adapter.get("kind") not in ("agent", "simulation") or not isinstance(adapter.get("command"), list) or not adapter["command"] or any(not isinstance(v, str) or not v for v in adapter["command"]):
        parser.error("Adapter must declare kind and a nonempty command argument list; shell strings are unsupported")
    plan = []
    for suite in suites:
        if args.skill and suite["skill"] not in args.skill:
            continue
        for case in suite["cases"]:
            if args.case and case["id"] not in args.case:
                continue
            for condition in (["candidate"] if case["mode"] == "routing" else ["baseline", "candidate"]):
                for trial in range(1, args.trials + 1):
                    plan.append((suite, case, condition, trial))
    if not plan or len(plan) > args.max_runs:
        parser.error(f"Selected {len(plan)} executions; choose cases within --max-runs={args.max_runs}")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    destination = args.output.resolve() / stamp
    results = []
    for suite, case, condition, trial in plan:
        result = run_trial(ROOT, suite, case, condition, trial, destination, adapter, args.timeout)
        results.append(result)
        print(f"{case['id']} {condition} trial {trial}: {result['verdict']['status']}", flush=True)
    report["behavioral"] = {
        "status": "executed" if adapter["kind"] == "agent" else "simulation",
        "mode": "paired-outcomes-and-selection", "cases": len({r['case_id'] for r in results}),
        **trial_counts(results, adapter["kind"]),
        "reason": "Artifact checks and trace observations are recorded; pending human rubric items prevent full quality certification.",
        "results": results,
        "summary": summarize(results),
    }
    write_json(destination / "report.json", report)
    print(destination / "report.json")
    return int(any(r["verdict"]["status"] in ("failed", "ungraded") for r in results))


if __name__ == "__main__":
    raise SystemExit(main())
