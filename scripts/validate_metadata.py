#!/usr/bin/env python3
from pathlib import Path
import re, sys

root = Path(__file__).resolve().parents[1]
errors = []
for folder in sorted((root / "skills").iterdir()):
    if not folder.is_dir(): continue
    try:
        text = (folder / "SKILL.md").read_text(encoding="utf-8")
    except (FileNotFoundError, UnicodeDecodeError) as exc:
        errors.append(folder.name + ": cannot read SKILL.md: " + str(exc))
        continue
    front = text.split("---", 2)[1] if text.startswith("---") else ""
    fields = dict(line.split(":", 1) for line in front.splitlines() if ":" in line)
    fields = {key.strip(): value.strip() for key, value in fields.items()}
    if fields.get("name") != folder.name: errors.append(folder.name + ": name mismatch")
    description = fields.get("description", "")
    if len(description) < 80 or "Use for " not in description or "do not use" not in description:
        errors.append(folder.name + ": description is not discriminating")
    if not re.fullmatch(r"\d+\.\d+\.\d+", fields.get("version", "")):
        errors.append(folder.name + ": invalid version")
    try:
        ui = (folder / "agents" / "openai.yaml").read_text(encoding="utf-8")
    except (FileNotFoundError, UnicodeDecodeError) as exc:
        errors.append(folder.name + ": cannot read openai.yaml: " + str(exc))
        continue
    match = re.search(r'^  short_description: "([^"]+)"$', ui, re.M)
    if not match or not 25 <= len(match.group(1)) <= 64:
        errors.append(folder.name + ": invalid UI short_description")
    if "Use $" + folder.name not in ui:
        errors.append(folder.name + ": invalid default prompt")
if errors:
    print("\n".join("ERROR " + error for error in errors)); sys.exit(1)
print("OK: metadata")
