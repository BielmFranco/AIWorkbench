#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def check(root=ROOT):
    skills = root / "skills"
    if not skills.is_dir():
        return ["Missing skills directory"]
    folders = [p for p in skills.iterdir() if p.is_dir() and not p.name.startswith(".")]
    if not folders:
        return ["Empty skill catalog"]
    return [folder.name + ": missing SKILL.md" for folder in folders if not (folder / "SKILL.md").is_file()]


if __name__ == "__main__":
    errors = check()
    print("\n".join("ERROR " + e for e in errors) if errors else "OK: discoverable skill directories")
    sys.exit(bool(errors))
