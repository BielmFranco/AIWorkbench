#!/usr/bin/env python3
from pathlib import Path
import re, sys

root = Path(__file__).resolve().parents[1]
errors = []
pattern = re.compile(r"\[[^]]*\]\(([^)]+)\)")
for source in root.rglob("*.md"):
    if any(part in {".git", "dist", ".venv", ".tmp", "runs"} for part in source.parts): continue
    try:
        text = source.read_text(encoding="utf-8")
    except (FileNotFoundError, UnicodeDecodeError) as exc:
        errors.append(str(source) + ": cannot read: " + str(exc))
        continue
    for raw in pattern.findall(text):
        target = raw.strip().split("#", 1)[0]
        if not target or target.startswith(("http://", "https://", "mailto:")): continue
        resolved = (source.parent / target).resolve()
        if not resolved.exists():
            errors.append(str(source.relative_to(root)) + ": missing link target " + target)
        if source.is_relative_to(root / "skills"):
            skill_folder = root / "skills" / source.relative_to(root / "skills").parts[0]
            if resolved.exists() and skill_folder not in resolved.parents and resolved != skill_folder:
                errors.append(str(source.relative_to(root)) + ": link escapes portable skill: " + target)
if errors:
    print("\n".join("ERROR " + error for error in errors)); sys.exit(1)
print("OK: relative links")
