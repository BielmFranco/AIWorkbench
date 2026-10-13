# Adapter protocol v1

An adapter is a trusted executable that reads one JSON request from stdin. Configuration declares `kind` as `agent` or `simulation` and `command` as a list of arguments; the runner executes it without a shell. Use the correct Python executable for your environment.

The request supplies `protocol_version`, `case_id`, `mode`, `condition`, `prompt`, `workspace`, `output_dir` and `observation_path`. The fixture files live at `workspace/fixtures`. Requested artifacts must be written under `output_dir`. The candidate has local skills under `.agents/skills`; the baseline has none. The request deliberately excludes grading criteria and control artifacts.

Exit nonzero on a failed provider invocation. Write an observation JSON object at the specified path, for example:

```json
{
  "adapter_kind": "agent",
  "model": "actual-model-id",
  "usage": null,
  "provider_turn_completed": null,
  "capture_complete": false,
  "resource_reads": []
}
```

Set `provider_turn_completed` to true only when the provider trace confirms a completed agent turn. False means no completed turn was observed; null or omission means unavailable. Reports count adapter attempts separately from confirmed live trials, so a missing executable or authentication failure does not inflate the live count.

When read instrumentation is available, entries in `resource_reads` contain `kind: resource_read`, `skill`, and a resolvable `trace_ref`. Set `capture_complete` only if all relevant resource reads were captured. A positive observed read may support selection; absence needs complete capture. Do not convert a string mentioning a path or the model's assertion into a read event.

## Codex adapter

Copy [codex.example.json](codex.example.json) to a local configuration, provide an authenticated dedicated `CODEX_HOME`, and select a fixed model when reproducibility requires it. The adapter does not copy credentials. It rejects custom global skills/plugins and skill directories in workspace ancestors to reduce baseline contamination, and uses the normal workspace-write sandbox with ephemeral execution and user configuration excluded.

The CLI event stream is saved as `events.jsonl`. Command-reference hints are retained for human inspection but are not certified read events: routing remains ungraded. Outcome artifacts are still graded. The dedicated home and fixture copy are not a complete host isolation boundary; use an isolated container/host with restricted read access for held-out or untrusted evaluation. The outer runner bounds and terminates the adapter process tree on timeout.

## Simulation adapters

`tests/fixture_adapter.py` is a harness-control adapter. It supplies known artifacts to test execution and isolation mechanics. Declare it as `simulation`; its output must never be described as model efficacy.
