# Architecture

AIWorkbench is a portable catalog. Each `skills/<name>/SKILL.md` is a discovery and instruction entrypoint. Domain resources load on demand. Deterministic scripts validate structure; behavioral evals remain separate.

```mermaid
flowchart LR
  Prompt --> Metadata[Name and description]
  Metadata --> Skill[SKILL.md]
  Skill --> Resources[References and templates]
  Skill --> Scripts[Deterministic scripts]
  Cases[Eval cases] --> Harness[Eval harness]
  Harness --> Report[Evidence report]
```
