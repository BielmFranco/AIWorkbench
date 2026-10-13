#!/usr/bin/env python3
import json, subprocess, sys
import os
from pathlib import Path

root = Path(__file__).resolve().parents[1]
checks = ["validate_structure.py", "validate_metadata.py", "validate_links.py", "validate_installers.py", "validate.py"]
results = []
for check in checks:
    run = subprocess.run([sys.executable, str(root / "scripts" / check)], cwd=root, text=True, capture_output=True)
    results.append((check, run.returncode, (run.stdout or run.stderr).strip()))
test_env = os.environ.copy()
temporary_root = root / ".tmp"
temporary_root.mkdir(exist_ok=True)
test_env["TEMP"] = str(temporary_root)
test_env["TMP"] = str(temporary_root)
test_run = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=root, text=True, capture_output=True, env=test_env)
results.append(("format, grader and runner controls", test_run.returncode, (test_run.stdout + test_run.stderr).strip()))
eval_run = subprocess.run([sys.executable, str(root / "scripts" / "run_evals.py")], cwd=root, text=True, capture_output=True)
latest = json.loads((root / "evals" / "reports" / "latest.json").read_text(encoding="utf-8"))
overall_status = "failed" if any(code for _, code, _ in results) or eval_run.returncode else "passed"
skills = sorted((root / "skills").glob("*/SKILL.md"))
skill_bytes = [path.stat().st_size for path in skills]
estimated_tokens = sum(skill_bytes) // 4
lines = [
  "# AIWorkbench validation report", "",
  "## Summary", "",
  "- Architecture: portable filesystem skills with progressive disclosure.",
  "- Skills: " + str(len(skills)),
  "- Evaluation cases: " + str(latest["deterministic"]["cases"]),
  "- Deterministic status: " + overall_status,
  "- Behavioral trials: " + latest["behavioral"]["status"], "",
  "## Catalog", "",
]
lines += ["- " + path.parent.name for path in skills]
lines += ["", "## Deterministic validation", "", "| Check | Status | Evidence |", "| --- | --- | --- |"]
for name, code, evidence in results:
    lines.append("| " + name + " | " + ("PASS" if code == 0 else "FAIL") + " | " + evidence.replace("|", "\\|").replace("\n", " ").replace("\r", "") + " |")
lines += [
  "", "## Evaluation", "",
  "- Suites: " + str(latest["deterministic"]["suites"]),
  "- Cases: " + str(latest["deterministic"]["cases"]),
  "- Behavioral trials: " + latest["behavioral"]["status"],
  "- Live-provider trials: " + str(latest["behavioral"]["live_trials"]),
  "- Policy: " + latest["behavioral"]["reason"], "",
  "## Context and performance indicators", "",
  "- Total SKILL.md bytes: " + str(sum(skill_bytes)),
  "- Smallest SKILL.md bytes: " + str(min(skill_bytes)),
  "- Largest SKILL.md bytes: " + str(max(skill_bytes)),
  "- Approximate catalog tokens if every full skill were loaded: " + str(estimated_tokens),
  "- Normal operation loads metadata first and full instructions only when routed.", "",
  "## Sources", "",
  "- Canonical source record: docs/sources.md",
  "- Architecture: docs/architecture.md",
  "- Quality standard: docs/quality-standard.md",
  "- Routing rules: docs/routing.md", "",
  "## Validation coverage", "",
  "- Deterministic CI validates structure, metadata, links, installers, cases, and packaging contracts.",
  "- Live-provider trials remain opt-in because they consume account usage and vary by model and harness.",
  "- Grader-control executions are simulations of known artifacts, not model efficacy measurements.",
  "- Independent scenario evidence, when available, is in evals/reports/forward-tests.md.",
  "- Product-specific upload availability is documented in docs/compatibility.md.", "",
  "## Next actions", "",
  "1. Run live-provider trials when a release needs model-specific certification.",
  "2. Calibrate subjective graders with blinded human review.",
  "3. Promote stable capability cases into a regression suite.", ""
]
output = root / "evals" / "reports" / "latest.md"
output.write_text("\n".join(lines), encoding="utf-8")
print(output.relative_to(root))
sys.exit(1 if any(code for _, code, _ in results) or eval_run.returncode else 0)
