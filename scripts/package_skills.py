#!/usr/bin/env python3
"""Create one portable ZIP per skill without external dependencies."""

from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
DIST = ROOT / "dist"


def available() -> list[Path]:
    if not SKILLS.is_dir():
        raise SystemExit(f"Diretório não encontrado: {SKILLS}")
    return sorted(path for path in SKILLS.iterdir() if (path / "SKILL.md").is_file())


def package(skill: Path) -> Path:
    DIST.mkdir(parents=True, exist_ok=True)
    output = DIST / f"{skill.name}.zip"
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        for path in sorted(skill.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(skill))
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Empacota skills do AIWorkbench.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true")
    group.add_argument("--skill")
    args = parser.parse_args()

    skills = available()
    if args.skill:
        skills = [path for path in skills if path.name == args.skill]
        if not skills:
            raise SystemExit(f"Skill desconhecida: {args.skill}")

    for skill in skills:
        print(package(skill).relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
