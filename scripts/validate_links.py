#!/usr/bin/env python3
from pathlib import Path
import re, sys

root = Path(__file__).resolve().parents[1]
errors = []
pattern = re.compile(r"\[[^]]*\]\(([^)]+)\)")
for source in root.rglob("*.md"):
    if any(part in {".git", "dist"} for part in source.parts): continue
    text = source.read_text(encoding="utf-8")
    for raw in pattern.findall(text):
        target = raw.strip().split("#", 1)[0]
        if not target or target.startswith(("http://", "https://", "mailto:")): continue
        resolved = (source.parent / target).resolve()
        if not resolved.exists():
            errors.append(str(source.relative_to(root)) + ": missing link target " + target)
if errors:
    print("\n".join("ERROR " + error for error in errors)); sys.exit(1)
print("OK: relative links")
