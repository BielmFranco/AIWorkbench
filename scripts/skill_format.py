"""Parse the public Agent Skills format without prescribing a prose layout."""
from pathlib import Path
import re

try:
    import yaml
except ImportError as exc:
    raise SystemExit("Install dependencies: python -m pip install -r requirements-dev.txt") from exc


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"Duplicate YAML key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)
ALLOWED_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}


def load_yaml(text):
    return yaml.load(text, Loader=UniqueLoader)


def parse_skill(path: Path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)(.*)\Z", text, re.S)
    if not match:
        raise ValueError("Expected YAML frontmatter delimited by ---")
    data = load_yaml(match.group(1))
    if not isinstance(data, dict):
        raise ValueError("Frontmatter must be a mapping")
    return data, match.group(2)


def validate_skill(path: Path):
    errors = []
    try:
        data, body = parse_skill(path)
    except (OSError, UnicodeError, ValueError, TypeError, yaml.YAMLError) as exc:
        return [str(exc)]
    extra = set(data) - ALLOWED_FIELDS
    if extra:
        errors.append(f"Unsupported frontmatter fields: {sorted(map(str, extra))}")
    name = data.get("name")
    if not isinstance(name, str) or not name or len(name) > 64 or name != name.lower() or name.startswith("-") or name.endswith("-") or "--" in name or not all(c.isalnum() or c == "-" for c in name):
        errors.append("name must be 1–64 lowercase letters/digits/hyphens without empty segments")
    elif name != path.parent.name:
        errors.append("name must match its directory")
    description = data.get("description")
    if not isinstance(description, str) or not 1 <= len(description.strip()) <= 1024:
        errors.append("description must be a nonempty string of at most 1024 characters")
    for field in ("license", "allowed-tools", "compatibility"):
        if field in data and (not isinstance(data[field], str) or not data[field].strip()):
            errors.append(field + " must be a nonempty string")
    if isinstance(data.get("compatibility"), str) and len(data["compatibility"]) > 500:
        errors.append("compatibility exceeds 500 characters")
    if "metadata" in data:
        metadata = data["metadata"]
        if not isinstance(metadata, dict) or any(not isinstance(k, str) or not isinstance(v, str) for k, v in metadata.items()):
            errors.append("metadata must map string keys to string values")
    if not body.strip():
        errors.append("Skill instructions are empty")
    return errors
