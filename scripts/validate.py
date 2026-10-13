#!/usr/bin/env python3
"""Validate portable metadata, resources, and executable evaluation specifications."""
import json
from pathlib import Path
import sys
from jsonschema import Draft202012Validator
from eval_grading import contained
from skill_format import parse_skill
import validate_structure
import validate_metadata

ROOT = Path(__file__).resolve().parents[1]


def check_cases(root=ROOT):
    schema = json.loads((root / "shared/schemas/eval-case.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    errors, ids, count = [], set(), 0
    for entry in sorted((root / "skills").glob("*/SKILL.md")):
        name = entry.parent.name
        try:
            metadata, _ = parse_skill(entry)
            suite = json.loads((root / "evals/cases" / f"{name}.json").read_text(encoding="utf-8"))
            if set(suite) != {"schema_version", "skill", "skill_version", "cases"}:
                raise ValueError("Unexpected or missing suite fields")
            if suite["schema_version"] != 2 or suite["skill"] != name or suite["skill_version"] != metadata.get("metadata", {}).get("version"):
                raise ValueError("Suite format, skill or version mismatch")
            if not isinstance(suite["cases"], list) or not suite["cases"]:
                raise ValueError("Empty or invalid case list")
            modes = set()
            for case in suite["cases"]:
                count += 1
                schema_errors = list(validator.iter_errors(case))
                if schema_errors:
                    errors.extend(f"{name}: {e.message}" for e in schema_errors)
                    continue
                cid = case["id"]
                if cid in ids:
                    errors.append("Duplicate case ID: " + cid)
                ids.add(cid)
                modes.add(case["mode"])
                if case["mode"] == "routing":
                    if case["skill_under_test"] != name or case["expected_skill"] not in (name, None):
                        errors.append(cid + ": invalid routing target")
                    continue
                if not contained(root, case["fixtures"]).is_dir():
                    errors.append(cid + ": missing fixtures")
                assertion_ids = set()
                for assertion in case["assertions"]:
                    if assertion["id"] in assertion_ids:
                        errors.append(cid + ": duplicate assertion ID")
                    assertion_ids.add(assertion["id"])
                    contained(root, assertion["artifact"])
                    for field in ("schema", "test"):
                        if field in assertion:
                            resource = contained(root, assertion[field])
                            if not resource.is_file():
                                errors.append(cid + ": missing " + field + " resource")
                            elif field == "schema":
                                Draft202012Validator.check_schema(json.loads(resource.read_text(encoding="utf-8")))
            if modes != {"routing", "outcome"}:
                errors.append(name + ": selection and outcome coverage both required")
        except (OSError, UnicodeError, ValueError, TypeError, KeyError) as exc:
            errors.append(f"{name}: {exc}")
    return errors, count


if __name__ == "__main__":
    errors = validate_structure.check() + validate_metadata.check()
    try:
        case_errors, count = check_cases()
        errors += case_errors
    except Exception as exc:
        errors.append("Case validation could not complete: " + str(exc))
        count = 0
    print("\n".join("ERROR " + e for e in errors) if errors else f"OK: {len(list((ROOT / 'skills').glob('*/SKILL.md')))} skills, {count} case specifications; behavior not executed")
    sys.exit(bool(errors))
