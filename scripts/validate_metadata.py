#!/usr/bin/env python3
from pathlib import Path
import sys
from skill_format import load_yaml, validate_skill, yaml

ROOT = Path(__file__).resolve().parents[1]


def check(root=ROOT):
    errors = []
    for folder in sorted((root / "skills").iterdir()):
        if not folder.is_dir() or folder.name.startswith("."):
            continue
        errors.extend(f"{folder.name}: {e}" for e in validate_skill(folder / "SKILL.md"))
        ui_file = folder / "agents" / "openai.yaml"
        if not ui_file.exists():
            continue
        try:
            ui = load_yaml(ui_file.read_text(encoding="utf-8"))
            if not isinstance(ui, dict) or not isinstance(ui.get("interface"), dict):
                raise ValueError("UI metadata must contain an interface mapping")
            interface = ui["interface"]
            for key in ("display_name", "short_description", "default_prompt"):
                if not isinstance(interface.get(key), str) or not interface[key].strip():
                    errors.append(f"{folder.name}: invalid {key}")
            short = interface.get("short_description", "")
            if isinstance(short, str) and not 25 <= len(short) <= 64:
                errors.append(f"{folder.name}: UI short_description must have 25–64 characters")
            prompt = interface.get("default_prompt", "")
            if isinstance(prompt, str) and "$" + folder.name not in prompt:
                errors.append(f"{folder.name}: default_prompt must mention the skill")
            policy = ui.get("policy", {})
            if not isinstance(policy, dict) or ("allow_implicit_invocation" in policy and not isinstance(policy["allow_implicit_invocation"], bool)):
                errors.append(f"{folder.name}: invalid invocation policy")
        except (OSError, UnicodeError, ValueError, TypeError, yaml.YAMLError) as exc:
            errors.append(f"{folder.name}: {exc}")
    return errors


if __name__ == "__main__":
    errors = check()
    print("\n".join("ERROR " + e for e in errors) if errors else "OK: Agent Skills format and UI metadata")
    sys.exit(bool(errors))
