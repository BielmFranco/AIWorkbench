# Independent forward-test evidence

Date: 2026-10-13. Skill version: 1.2.0. These are three independent scenario executions using the session's configured default model, without a pinned model ID or controlled baseline. They provide limited evidence of instruction clarity and requested-mode adherence, not comparative efficacy or certification of all 15 skills.

| Skill | Raw request | Observed outcome | Scope limit |
| --- | --- | --- | --- |
| ai-agent-engineer | Design an authorized refund assistant with a provider that can time out; give bounded recovery and failure tests. | Selected a deterministic service baseline, kept authorization in the service, preserved request keys, bounded attempts and unresolved escalation. | Design only; no provider or failure test ran. |
| code-review-and-refactoring-expert | Review the supplied 50-to-500 pagination fallback against its public contract; do not edit. | Reported one P2 contract defect at the changed fallback and excluded unspecified input behavior. | Supplied snippets only; no runtime or code edit. |
| tech-lead | Plan account-read migration across service/platform teams with p95 <150 ms and zero unexplained mismatches; writes remain in monolith. | Proposed vertical milestones, dependencies, ownership, rollout signals and original-read-path recovery; unknown dates remained unknown. | Plan only; no rollout, telemetry or load execution. |

Read the preserved outputs: [agent design](forward-tests/agent-design.md), [review](forward-tests/review.md), [delivery plan](forward-tests/plan.md). No evaluator received an intended answer. The supplied scenarios resemble public worked examples, so they are development forward checks rather than held-out generalization evidence. No instruction confusion was reported by the evaluators. Parent review checked the actual artifacts against the requested modes and constraints.

## Infrastructure review

An independent reviewer examined the parser, runner, graders, adapter and controls. Findings led to fixes for candidate termination spoofing, malformed observation handling, run-path containment, unsupported YAML keys and false resource-read inference. A subsequent recheck caught loss of Python return-type semantics in the JSON worker transport; the transport now preserves tuple/set return types, with a regression test for a contract-breaking tuple.

The deterministic suite covers these regressions, accepts known correct artifacts and valid alternatives, rejects corrupt/incomplete artifacts, and labels adapter simulations separately. Worker isolation preserves grader control flow but does not make untrusted code safe without an external execution sandbox.

The final focused recheck closed the remaining return-type and process-lifetime findings. RAG accepts its permitted list/tuple/set alternatives and rejects dictionaries; Windows job ownership is established before a child starts and retains descendants after their parent exits. No unresolved finding remained from that scoped review. This is infrastructure-review evidence, not an agent performance result.
