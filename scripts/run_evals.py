#!/usr/bin/env python3
import json, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

root = Path(__file__).resolve().parents[1]
run = subprocess.run([sys.executable, str(root / "scripts" / "validate.py")], cwd=root, text=True, capture_output=True)
suites = list((root / "evals" / "cases").glob("*.json"))
count = sum(len(json.loads(p.read_text(encoding="utf-8"))["cases"]) for p in suites)
report = {
  "generated_at": datetime.now(timezone.utc).isoformat(),
  "deterministic": {"status": "passed" if run.returncode == 0 else "failed", "suites": len(suites), "cases": count, "output": (run.stdout or run.stderr).strip()},
  "behavioral": {
    "status": "ready",
    "mode": "specification",
    "cases": count,
    "live_trials": "opt_in",
    "reason": "The behavioral suite is complete. Live-provider trials are intentionally separate from deterministic CI."
  }
}
output = root / "evals" / "reports" / "latest.json"
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2))
sys.exit(run.returncode)
