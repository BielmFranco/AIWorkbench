# AIWorkbench validation report

## Summary

- Architecture: portable filesystem skills with progressive disclosure.
- Skills: 15
- Evaluation cases: 75
- Deterministic status: passed
- Behavioral trials: not_run

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
| validate_structure.py | PASS | OK: discoverable skill directories |
| validate_metadata.py | PASS | OK: Agent Skills format and UI metadata |
| validate_links.py | PASS | OK: relative links |
| validate_installers.py | PASS | OK: installers and portable ZIPs (15/15) |
| validate.py | PASS | OK: 15 skills, 75 case specifications; behavior not executed |
| format, grader and runner controls | PASS | test_all_known_controls_and_corrupt_outputs (test_eval_grading.GraderTests.test_all_known_controls_and_corrupt_outputs) ... ok test_candidate_cannot_skip_checks_by_exiting_with_a_pass_marker (test_eval_grading.GraderTests.test_candidate_cannot_skip_checks_by_exiting_with_a_pass_marker) ... ok test_equal_json_numbers_allow_float_but_not_boolean (test_eval_grading.GraderTests.test_equal_json_numbers_allow_float_but_not_boolean) ... ok test_path_escape_is_rejected (test_eval_grading.GraderTests.test_path_escape_is_rejected) ... ok test_rag_grader_rejects_dictionary_as_passage_sequence (test_eval_grading.GraderTests.test_rag_grader_rejects_dictionary_as_passage_sequence) ... ok test_selection_needs_trace_not_self_report (test_eval_grading.GraderTests.test_selection_needs_trace_not_self_report) ... ok test_worker_accepts_a_valid_unordered_iterable (test_eval_grading.GraderTests.test_worker_accepts_a_valid_unordered_iterable) ... ok test_worker_preserves_return_type_contract (test_eval_grading.GraderTests.test_worker_preserves_return_type_contract) ... ok test_case_path_cannot_escape_destination (test_eval_runner.RunnerTests.test_case_path_cannot_escape_destination) ... ok test_live_trials_require_provider_completion (test_eval_runner.RunnerTests.test_live_trials_require_provider_completion) ... ok test_malformed_observation_records_failure (test_eval_runner.RunnerTests.test_malformed_observation_records_failure) ... ok test_paired_workspace_isolation_and_simulation_label (test_eval_runner.RunnerTests.test_paired_workspace_isolation_and_simulation_label) ... ok test_timeout_cleans_descendant_after_parent_exit (test_process_control.ProcessTests.test_timeout_cleans_descendant_after_parent_exit) ... ok test_timeout_stops_the_execution (test_process_control.ProcessTests.test_timeout_stops_the_execution) ... ok test_duplicate_key_is_rejected (test_skill_format.FormatTests.test_duplicate_key_is_rejected) ... ok test_mixed_unknown_keys_are_errors_not_crashes (test_skill_format.FormatTests.test_mixed_unknown_keys_are_errors_not_crashes) ... ok test_top_level_version_is_rejected (test_skill_format.FormatTests.test_top_level_version_is_rejected) ... ok test_types_and_limits (test_skill_format.FormatTests.test_types_and_limits) ... ok test_valid_metadata_and_multiline_description (test_skill_format.FormatTests.test_valid_metadata_and_multiline_description) ... ok  ---------------------------------------------------------------------- Ran 19 tests in 11.437s  OK |

## Evaluation

- Suites: 15
- Cases: 75
- Behavioral trials: not_run
- Live-provider trials: 0
- Policy: No adapter selected; no agent or behavioral outcome was executed.

## Context and performance indicators

- Total SKILL.md bytes: 38667
- Smallest SKILL.md bytes: 2476
- Largest SKILL.md bytes: 2711
- Approximate catalog tokens if every full skill were loaded: 9666
- Normal operation loads metadata first and full instructions only when routed.

## Sources

- Canonical source record: docs/sources.md
- Architecture: docs/architecture.md
- Quality standard: docs/quality-standard.md
- Routing rules: docs/routing.md

## Validation coverage

- Deterministic CI validates structure, metadata, links, installers, cases, and packaging contracts.
- Live-provider trials remain opt-in because they consume account usage and vary by model and harness.
- Grader-control executions are simulations of known artifacts, not model efficacy measurements.
- Independent scenario evidence, when available, is in evals/reports/forward-tests.md.
- Product-specific upload availability is documented in docs/compatibility.md.

## Next actions

1. Run live-provider trials when a release needs model-specific certification.
2. Calibrate subjective graders with blinded human review.
3. Promote stable capability cases into a regression suite.
