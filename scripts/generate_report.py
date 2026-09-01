#!/usr/bin/env python3
import json, subprocess, sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
checks = ["validate_structure.py", "validate_metadata.py", "validate_links.py", "validate.py"]
results = []
for check in checks:
    run = subprocess.run([sys.executable, str(root / "scripts" / check)], cwd=root, text=True, capture_output=True)
    results.append((check, run.returncode, (run.stdout or run.stderr).strip()))
eval_run = subprocess.run([sys.executable, str(root / "scripts" / "run_evals.py")], cwd=root, text=True, capture_output=True)
latest = json.loads((root / "evals" / "reports" / "latest.json").read_text(encoding="utf-8"))
skills = sorted((root / "skills").glob("*/SKILL.md"))
skill_bytes = [path.stat().st_size for path in skills]
estimated_tokens = sum(skill_bytes) // 4
lines = [
  "# AIWorkbench validation report", "",
  "## Summary", "",
  "- Architecture: portable filesystem skills with progressive disclosure.",
  "- Skills: " + str(len(skills)),
  "- Evaluation cases: " + str(latest["deterministic"]["cases"]),
  "- Deterministic status: " + latest["deterministic"]["status"],
  "- Behavioral status: " + latest["behavioral"]["status"], "",
  "## Catalog", "",
]
lines += ["- " + path.parent.name for path in skills]
lines += ["", "## Deterministic validation", "", "| Check | Status | Evidence |", "| --- | --- | --- |"]
for name, code, evidence in results:
    lines.append("| " + name + " | " + ("PASS" if code == 0 else "FAIL") + " | " + evidence.replace("|", "\\|") + " |")
lines += [
  "", "## Evaluation", "",
  "- Suites: " + str(latest["deterministic"]["suites"]),
  "- Cases: " + str(latest["deterministic"]["cases"]),
  "- Behavioral: " + latest["behavioral"]["status"],
  "- Limitation: " + latest["behavioral"]["reason"], "",
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
  "## Unverified items and risk", "",
  "- Behavioral pass rate is not claimed without model trials and traces.",
  "- Bash installer syntax was not verified when Bash is unavailable on the host.",
  "- Product-specific upload availability depends on provider and account.", "",
  "## Next actions", "",
  "1. Run representative behavioral trials in a configured Codex or Claude harness.",
  "2. Calibrate subjective graders with blinded human review.",
  "3. Promote stable capability cases into a regression suite.", ""
]
output = root / "evals" / "reports" / "latest.md"
output.write_text("\n".join(lines), encoding="utf-8")
print(output.relative_to(root))
sys.exit(1 if any(code for _, code, _ in results) or eval_run.returncode else 0)
