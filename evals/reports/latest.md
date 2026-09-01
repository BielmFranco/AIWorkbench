# AIWorkbench validation report

## Summary

- Architecture: portable filesystem skills with progressive disclosure.
- Skills: 15
- Evaluation cases: 120
- Deterministic status: passed
- Behavioral suite: ready

## Catalog

- ai-agent-engineer
- ai-evaluation-engineer
- ai-product-strategist
- code-review-and-refactoring-expert
- context-and-prompt-engineer
- design-system-architect
- frontend-experience-engineer
- full-stack-architect
- performance-and-reliability-engineer
- premium-ui-designer
- rag-knowledge-engineer
- security-and-guardrails-engineer
- senior-software-engineer
- tech-lead
- ux-product-designer

## Deterministic validation

| Check | Status | Evidence |
| --- | --- | --- |
| validate_structure.py | PASS | OK: structure |
| validate_metadata.py | PASS | OK: metadata |
| validate_links.py | PASS | OK: relative links |
| validate_installers.py | PASS | OK: install.ps1 and install.sh syntax and all-skills copy (15/15) |
| validate.py | PASS | OK: 15 skills, 120 eval cases |

## Evaluation

- Suites: 15
- Cases: 120
- Behavioral specification: ready
- Live-provider trials: opt_in
- Policy: The behavioral suite is complete. Live-provider trials are intentionally separate from deterministic CI.

## Context and performance indicators

- Total SKILL.md bytes: 47381
- Smallest SKILL.md bytes: 2995
- Largest SKILL.md bytes: 3265
- Approximate catalog tokens if every full skill were loaded: 11845
- Normal operation loads metadata first and full instructions only when routed.

## Sources

- Canonical source record: docs/sources.md
- Architecture: docs/architecture.md
- Quality standard: docs/quality-standard.md
- Routing rules: docs/routing.md

## Validation coverage

- Deterministic CI validates structure, metadata, links, installers, cases, and packaging contracts.
- Live-provider trials remain opt-in because they consume account usage and vary by model and harness.
- Product-specific upload availability is documented in docs/compatibility.md.

## Next actions

1. Run live-provider trials when a release needs model-specific certification.
2. Calibrate subjective graders with blinded human review.
3. Promote stable capability cases into a regression suite.
