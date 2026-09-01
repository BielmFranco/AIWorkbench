#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
expected = ['ai-product-strategist', 'tech-lead', 'full-stack-architect', 'senior-software-engineer', 'frontend-experience-engineer', 'premium-ui-designer', 'design-system-architect', 'ux-product-designer', 'ai-agent-engineer', 'context-and-prompt-engineer', 'rag-knowledge-engineer', 'ai-evaluation-engineer', 'security-and-guardrails-engineer', 'performance-and-reliability-engineer', 'code-review-and-refactoring-expert']
resources = ["SKILL.md", "README.md", "agents/openai.yaml", "references/practice-guide.md", "checklists/release.md", "templates/deliverable.md", "examples/cases.md", "scripts/verify.py"]
errors = []
folders = sorted(p.name for p in (root / "skills").iterdir() if p.is_dir())
if folders != sorted(expected): errors.append("catalog does not contain exactly the expected 15 skills")
for name in expected:
    for resource in resources:
        if not (root / "skills" / name / resource).is_file():
            errors.append(name + ": missing " + resource)
if errors:
    print("\n".join("ERROR " + error for error in errors)); sys.exit(1)
print("OK: structure")
