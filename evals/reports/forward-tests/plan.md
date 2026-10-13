# Account-read migration delivery plan

Status: proposed plan; no rollout has run and no dates are agreed. Team ownership below is a proposed allocation to the two available teams. Individual decision makers and release authority remain unassigned. No duration or completion date is estimated.

## Outcome, scope, and evidence

Move the agreed account-read endpoints from the monolith to a service while preserving their authorization, response semantics, and account-data correctness. Writes remain in the monolith, which remains the authoritative write source and recovery read path.

The agreed gates are **p95 <150 ms** and **zero unexplained account-data mismatch**. Define the latency measurement boundary, evaluation window, minimum sample size, representative traffic mix, and comparison coverage before evaluating either gate. Proposed latency boundary: the complete user-facing read request, including routing and service dependencies. Evaluate each migrated endpoint and rollout cohort so an aggregate cannot hide a slow or incorrect path. Decisions on windows and sample sizes are pending; no successful gate is claimed.

Excluded: moving writes, changing account behavior, removing the monolith read path, and database rollback. Storage or replication design for service reads is unresolved. Do not assume an existing replica, event stream, or consistency guarantee.

## Decision ownership

| Class | Decision | Accountable owner | Required by |
| --- | --- | --- | --- |
| Product | In-scope reads, required freshness and read-after-write behavior, permitted response differences | Product decision owner: unassigned; service team supplies behavior inventory | M0 exit |
| Technical | Service source of truth for reads, replication if needed, snapshot/version comparison, authorization contract | Service technical decision owner: unassigned; platform team reviews infrastructure implications | M0 exit |
| Technical | Latency boundary, comparison coverage, evaluation windows/sample sizes, error and capacity gates | Platform technical decision owner: unassigned; service owner and product owner approve relevant semantics | Before M1 evaluation |
| Implementation | Service endpoints, contracts, correctness fixes | Service team; individual lead unassigned | Respective milestone exits |
| Implementation | Routing, telemetry, shadow isolation, feature flags, recovery controls | Platform team; individual lead unassigned | Respective milestone exits |
| Release | Traffic stages, observation periods, go/no-go, incident coordination | Release owner: unassigned | Before M3 rehearsal |

Assign the missing decision roles at M0. Proposed stop authority: either team's designated on-call engineer can stop or restore reads immediately; promotion requires the release owner's recorded approval and both teams' gate evidence. This authority must be explicitly agreed before live rollout. Deadlines are dependency gates, not calendar dates.

## Milestones and dependencies

| Milestone and usable result | Delivery owner | Depends on | Independently verifiable exit evidence | Decision needed |
| --- | --- | --- | --- | --- |
| M0: Agreed migration contract for a representative account-read slice | Service team, with platform team | Endpoint/consumer inventory; monolith behavior and authorization inspection; decision roles assigned | Reviewed endpoint map, consistency contract, dependency map, baseline latency/error/load evidence, and testable equivalence rules | Product scope and freshness; technical data source and authority |
| M1: First read works through the service in a controlled environment | Service team | M0; service data access and stable account identity | Representative authorized reads match monolith at the same logical version; denied requests remain denied; create/update/delete and immediate post-write reads meet the agreed contract; load evaluation meets latency gate | Approve first slice and evaluation specification |
| M2: Real traffic can be shadowed and compared without changing user responses | Platform team; service team resolves differences | M1; comparator, correlation/version metadata, isolated shadow capacity | Dashboard reports coverage, comparison failures, mismatch reasons and latency; alert probes work; zero unexplained mismatches over the approved window/sample; shadow failures do not affect primary reads | Approve shadow eligibility, sampling, and readiness evidence |
| M3: A bounded cohort can use service reads and recover to monolith reads | Platform team; service team supports recovery | M2; routing flag; staffed stop authority; monolith capacity retained | Recovery rehearsal demonstrates route restoration, in-flight request behavior, functional reads after restoration, and recovery time within an agreed objective; gated cohort configuration reviewed | Release owner approves stage schedule and recovery objective |
| M4: First slice serves users at increasing traffic levels | Platform team coordinates; service team owns service health | M3; approved windows/sample sizes and capacity/error gates | At every stage, user-facing p95 <150 ms, zero unexplained mismatches, approved health gates pass, and both teams record evidence before promotion | Release owner approves each promotion |
| M5: All agreed reads use the service with an operational handoff | Service team; platform team owns routing/operations | M4; M1–M4 repeated for remaining slices; endpoint-specific evidence | All in-scope reads pass gates at full planned load through the agreed observation window; runbooks, alert ownership and retained recovery path verified | Release owner accepts completion; product owner accepts scope |

Critical path: M0 → M1 → M2 → M3 → M4 → M5. Access to authoritative account data, trustworthy comparison, agreed consistency semantics, and assigned release authority can block this chain. After M0, platform telemetry/routing work can proceed alongside service implementation; both must converge before M2. Additional endpoints require their own contract and evidence, even if infrastructure is reused.

## Correctness and telemetry

Compare authorization outcome and the complete agreed account response, including null/missing fields, deletion state and errors. Normalize only explicitly approved nondeterministic fields; keep original responses accessible under approved data-handling controls. An explanation must have reproducible evidence and owner approval. Label missing versions, unavailable comparisons, or failed shadow reads as unverified, rather than matches. Report matched, mismatched, excluded, and unverified requests as separate counts and coverage rates.

Concurrent monolith writes can change data between reads. Use a common snapshot/version or another validated comparison method that detects genuine drift without mistaking two legitimate versions for equality. If service replication is selected, instrument lag and test post-write behavior; any exception to required freshness needs product approval. A replication delay is not automatically an acceptable mismatch.

Platform owns dashboards and alerts for end-to-end latency, endpoint/cohort p95, request/error/timeout rates, comparison counts/coverage, routing/fallback rate, service/dependency saturation, and replication lag if applicable. Service owns diagnosis of semantic differences and data-access failures. Record deployment/configuration versions with stage evidence. Health thresholds beyond the two agreed gates must be defined from the baseline and approved before rollout.

## Rollout and recovery

Proposed progression for each slice: shadow → small bounded production cohort → larger cohorts → full traffic. A candidate schedule is 5% → 25% → 50% → 100%; these percentages and dwell periods are proposals requiring release-owner agreement. Keep account assignments stable where needed to preserve a user's consistency expectations. Each stage must cover the approved traffic mix, observation period, minimum samples and expected load; elapsed time alone does not establish readiness.

At each stage, retain comparison coverage sufficient to enforce correctness and record a go/no-go decision. Stop promotion on incomplete evidence. Proposed immediate stop/restore triggers are any unexplained account-data mismatch, authorization divergence, a qualifying evaluation with p95 ≥150 ms, approved error/capacity gate failure, or lost required comparison/health telemetry. Configure evaluation windows before rollout so operators do not improvise thresholds during an incident.

Recovery procedure:

1. The agreed stop authority freezes promotion and routes the affected migrated reads back to the monolith using the verified routing control; broaden restoration if the fault boundary is unknown.
2. Platform confirms routing convergence, in-flight behavior, monolith capacity, and restored latency/error health; service verifies account responses and authorization on the restored path.
3. Preserve request correlations, versions, comparison evidence and configuration history for diagnosis. Disable shadow load if it contributes to the incident.
4. Service identifies and fixes the cause; platform repairs any routing/observability fault. Repeat relevant correctness checks and shadow evidence before the release owner authorizes a new canary.

Writes stay in the monolith throughout. Recovery restores the read route; it does not roll back account writes. Ensure service reads have no business-data side effects. Any service projection is repaired or rebuilt separately after reads have recovered. Keep monolith read capacity available until a separately authorized retirement decision.

## Risks and pending evidence

| Failure scenario | Observable signal | Mitigation / dependency | Owner | Decision deadline / residual consequence |
| --- | --- | --- | --- | --- |
| Replica or cache serves stale data after a write | Version lag; post-write mismatch | Decide freshness contract and data path; validate invalidation/replication if used | Service team | M0; unresolved freshness blocks service cutover |
| Authorization or response semantics drift | Denied/allowed divergence; field/error mismatch | Contract tests and comparable authorized shadow requests | Service team | M1; divergence requires restoration |
| Shadow comparison hides missing coverage or timing races | Unverified count, coverage gaps, inconsistent versions | Version-aware comparator; explicit exclusions and minimum coverage | Platform team with service team | M2; insufficient evidence blocks promotion |
| Service dependencies exceed latency or capacity budget | Cohort p95, timeouts, saturation | Representative load evaluation; capacity headroom and bounded stages | Service team; platform infrastructure support | M3; user latency may regress until restoration |
| Monolith cannot absorb restored traffic | Recovery rehearsal/load results | Retain capacity; validate restoration under projected load | Platform team | M3; no live cutover until recovery works |
| Stop controls or decision authority are unavailable | Failed flag/alert rehearsal; unstaffed stage | Verify controls, assign release/on-call roles, rehearse escalation | Platform team | M3; live rollout remains blocked |

Actual evidence for this deliverable: the supplied tech-lead skill, practice guide, worked example, and template were read; the plan was checked against the requested budgets, explicit dependency/owner requirements, and rollout/recovery requirements. No current-system validation, load test, shadow run, recovery rehearsal, or production rollout has occurred. No dates are agreed. Those missing results are milestone evidence to collect, not completed outcomes.

Skill instruction clarity: no confusing or conflicting instructions were identified. The instruction to mark unknown ownership is applied to individual decision and release roles; available-team allocations are explicitly proposed.
