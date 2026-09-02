#!/usr/bin/env python3
import json, re, sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
expected = ['ai-product-strategist', 'tech-lead', 'full-stack-architect', 'senior-software-engineer', 'frontend-experience-engineer', 'premium-ui-designer', 'design-system-architect', 'ux-product-designer', 'ai-agent-engineer', 'context-and-prompt-engineer', 'rag-knowledge-engineer', 'ai-evaluation-engineer', 'security-and-guardrails-engineer', 'performance-and-reliability-engineer', 'code-review-and-refactoring-expert']
sections = ['Purpose', 'Trigger Conditions', 'Non-Trigger Conditions', 'Required Inputs', 'Workflow', 'Decision Framework', 'Rules', 'Deliverables', 'Verification', 'Failure Handling', 'Quality Checklist', 'Examples', 'References']
resources = ["README.md", "agents/openai.yaml", "references/practice-guide.md", "checklists/release.md", "templates/deliverable.md", "examples/cases.md", "scripts/verify.py"]
errors, ids = [], set()
found = sorted(p.name for p in (root / "skills").iterdir() if p.is_dir())
if found != sorted(expected): errors.append("skill catalog mismatch")
for name in expected:
    folder, entry = root / "skills" / name, root / "skills" / name / "SKILL.md"
    if not entry.is_file(): errors.append(name + ": missing SKILL.md"); continue
    text = entry.read_text(encoding="utf-8")
    if not re.search(r"^name:\s*" + re.escape(name) + r"\s*$", text, re.M): errors.append(name + ": invalid name")
    for section in sections:
        if "## " + section not in text: errors.append(name + ": missing " + section)
    if "$" + name not in text or "/" + name not in text: errors.append(name + ": missing invocation")
    for resource in resources:
        if not (folder / resource).is_file(): errors.append(name + ": missing " + resource)
    try:
        data = json.loads((root / "evals" / "cases" / (name + ".json")).read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        errors.append(name + ": " + str(exc)); continue
    cases = data.get("cases", [])
    counts = {k: sum(c.get("type") == k for c in cases) for k in ("positive", "negative", "adversarial")}
    if counts != {"positive": 4, "negative": 2, "adversarial": 2}: errors.append(name + ": bad eval distribution")
    required_case_fields = ["id", "skill_expected", "type", "input", "context", "expected_behavior", "forbidden_behavior", "expected_artifacts", "success_criteria", "grader"]
    valid_types = {"positive", "negative", "adversarial"}
    for case in cases:
        cid = case.get("id", "unknown")
        if cid in ids: errors.append("duplicate " + cid)
        ids.add(cid)
        for field in required_case_fields:
            if field not in case: errors.append(cid + ": missing field " + field)
        if case.get("type") not in valid_types: errors.append(cid + ": invalid type " + str(case.get("type")))
        for str_field in ("id", "input", "context", "expected_behavior", "forbidden_behavior"):
            if str_field in case and isinstance(case[str_field], str) and not case[str_field]: errors.append(cid + ": empty " + str_field)
        for arr_field in ("success_criteria", "grader"):
            if arr_field in case and isinstance(case[arr_field], list) and not case[arr_field]: errors.append(cid + ": empty " + arr_field)
        extra = set(case.keys()) - set(required_case_fields)
        if extra: errors.append(cid + ": unexpected fields " + str(extra))
if errors:
    print("\n".join("ERROR " + e for e in errors)); sys.exit(1)
print("OK: %d skills, %d eval cases" % (len(expected), len(ids)))
