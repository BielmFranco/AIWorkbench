# Worked example: read-path migration

## Input
Two teams must move account reads from a monolith to a service. Writes remain in the monolith. The agreed target is p95 below 150 ms and no account-data mismatch.

| Milestone | Dependency | Owner | Exit evidence |
| --- | --- | --- | --- |
| Shadow one account read | Stable account ID and authorization contract | Service team | Same authorized response on representative fixtures |
| Compare shadow traffic | Comparison telemetry | Platform team | Zero unexplained mismatches in the agreed window |
| Shift 5% then 25% | Health dashboard and stop authority | Release owner | Meets latency/error budget at each stage |

## Decision
Stop on an unexplained data mismatch; restore monolith reads. Do not describe a database rollback because this slice does not move writes. The window and exact traffic schedule remain decisions for the owner, not invented facts.
