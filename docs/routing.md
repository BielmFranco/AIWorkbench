# Routing

Explicit invocation selects the named skill. Without explicit invocation, route by the primary outcome:

| Need | Primary skill | Boundary |
| --- | --- | --- |
| Validate product value | ai-product-strategist | Before delivery planning |
| Plan delivery | tech-lead | Milestones, owners, rollout |
| Design system boundaries | full-stack-architect | Before implementation detail |
| Implement production code | senior-software-engineer | After behavior is understood |
| Implement web experience | frontend-experience-engineer | Code, states, accessibility |
| Set premium visual direction | premium-ui-designer | Visual judgment, not code ownership |
| Govern reusable UI primitives | design-system-architect | Tokens, components, adoption |
| Improve task flow | ux-product-designer | Journey and usability |
| Build autonomous tool use | ai-agent-engineer | Agents, tools, state, recovery |
| Control instructions and context | context-and-prompt-engineer | Prompt contracts and evals |
| Retrieve grounded knowledge | rag-knowledge-engineer | Ingestion, retrieval, citations |
| Measure AI behavior | ai-evaluation-engineer | Tasks, trials, graders, outcomes |
| Assess security risk | security-and-guardrails-engineer | Trust and enforcement boundaries |
| Measure performance or reliability | performance-and-reliability-engineer | Baselines, profiles, load |
| Review or preserve behavior while restructuring | code-review-and-refactoring-expert | Review-only versus authorized edits |

Cross-cutting skills compose only when their concern is requested or materially affects the outcome. Product precedes planning; planning precedes architecture; architecture precedes implementation. UX defines flow, premium UI defines visual direction, design systems define reuse, and frontend engineering implements the experience.
