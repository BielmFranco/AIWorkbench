# AIWorkbench validation report

## Summary

- Architecture: portable filesystem skills with progressive disclosure.
- Skills: 15
- Evaluation cases: 120
- Deterministic status: passed
- Behavioral status: not_run

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
| validate.py | PASS | OK: 15 skills, 120 eval cases |

## Evaluation

- Suites: 15
- Cases: 120
- Behavioral: not_run
- Limitation: No model or agent harness configured; static checks do not prove behavior.

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

## Unverified items and risk

- Behavioral pass rate is not claimed without model trials and traces.
- Bash installer syntax was not verified when Bash is unavailable on the host.
- Product-specific upload availability depends on provider and account.

## Next actions

1. Run representative behavioral trials in a configured Codex or Claude harness.
2. Calibrate subjective graders with blinded human review.
3. Promote stable capability cases into a regression suite.
