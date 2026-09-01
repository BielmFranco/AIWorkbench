#!/usr/bin/env python3
from pathlib import Path
root = Path(__file__).resolve().parents[1]
required = ["SKILL.md", "README.md", "agents/openai.yaml", "references/practice-guide.md", "checklists/release.md", "templates/deliverable.md", "examples/cases.md"]
missing = [p for p in required if not (root / p).is_file()]
if missing:
    print("Missing: " + ", ".join(missing)); raise SystemExit(1)
print("security-and-guardrails-engineer: OK")
