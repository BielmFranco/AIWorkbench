#!/usr/bin/env python3
"""Adapter protocol v1 for an authenticated, isolated Codex evaluation environment."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=Path, required=True, help="Dedicated authenticated CODEX_HOME, without custom skills/plugins")
    parser.add_argument("--model", help="Optional fixed model; recorded in the observation")
    args = parser.parse_args()
    request = json.load(sys.stdin)
    home = args.home.resolve()
    workspace = Path(request["workspace"]).resolve()
    if not home.is_dir():
        parser.error("Dedicated CODEX_HOME does not exist; configure authentication in that environment first")
    for path in (home / "skills", home / "plugins", Path.home() / ".agents/skills"):
        if path.exists() and any(path.iterdir()):
            parser.error(f"Unexpected global skill/plugin resources contaminate the baseline: {path}")
    for ancestor in workspace.parents:
        for folder in (ancestor / ".agents/skills", ancestor / ".codex/skills"):
            if folder.exists() and any(folder.iterdir()):
                parser.error(f"Ancestor skill directory contaminates evaluation: {folder}")
    executable = shutil.which("codex")
    if not executable:
        parser.error("codex executable not found")
    environment = os.environ.copy()
    environment["CODEX_HOME"] = str(home)
    trace = Path(request["observation_path"]).parent / "events.jsonl"
    prompt = request["prompt"]
    if request["mode"] == "routing":
        prompt += "\nThis is a selection-only evaluation: inspect the relevant available skill if useful, and describe the intended approach. Do not implement the user task or call external services."
    else:
        prompt += "\nUse the available local skill when relevant. The task is restricted to this fixture workspace. Write requested artifacts under output/. Do not access live systems or credentials."
    command = [executable, "exec", "--ignore-user-config", "--ephemeral", "--skip-git-repo-check", "--sandbox", "workspace-write", "--cd", str(workspace), "--json", "-"]
    if args.model:
        command[2:2] = ["--model", args.model]
    with trace.open("w", encoding="utf-8") as stdout:
        code = subprocess.run(command, input=prompt, stdout=stdout, stderr=sys.stderr, text=True, encoding="utf-8", env=environment).returncode
    reads, usage, observed_types = [], None, set()
    provider_turn_completed = False
    for line_number, line in enumerate(trace.read_text(encoding="utf-8").splitlines(), 1):
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if event.get("type") == "turn.completed":
            provider_turn_completed = True
            usage = event.get("usage")
        item = event.get("item", {})
        if event.get("type") != "item.completed":
            continue
        observed_types.add(item.get("type"))
        if item.get("type") == "command_execution" and item.get("exit_code") == 0:
            text = item.get("command", "")
            matches = re.findall(r"(?:\.agents[\\/]+)?skills[\\/]+([a-z0-9-]+)[\\/]+SKILL\.md", text, flags=re.I)
            output = item.get("aggregated_output", "")
            for name in matches:
                if re.search(r"(?m)^name:\s*[\"']?" + re.escape(name) + r"[\"']?\s*$", output, re.I):
                    reads.append({"skill": name.lower(), "trace_ref": f"events.jsonl:{line_number}", "kind": "command_reference_hint"})
    # Positive command evidence is retained. Unknown read-capable tools prevent
    # asserting absence; do not infer activation from the agent's final prose.
    observation = {"resource_reads": [], "resource_read_hints": reads, "capture_complete": False, "usage": usage, "model": args.model or "configured-default", "adapter_kind": "agent", "provider_turn_completed": provider_turn_completed, "selection_limit": "Command-reference heuristics are hints for human inspection, not certified read events. Routing remains ungraded with this adapter."}
    Path(request["observation_path"]).write_text(json.dumps(observation, indent=2) + "\n", encoding="utf-8")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
