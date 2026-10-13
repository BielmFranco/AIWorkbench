# Planning a delivery that can be verified

## Scope and milestones
Start from an outcome, such as customers being able to use organization roles. Separate non-goals and unresolved product choices. Prefer vertical slices that demonstrate one user result, not lists such as 'database, backend, frontend' with no usable milestone.

For each milestone record dependencies, owner or role to be assigned, exit evidence, and the decision required to proceed. Expose the dependency chain that controls completion. If estimating, name the sizing method, assumptions, uncertainty, and calibration source; do not turn an unknown into a precise date.

## Rollout example
A read migration can start with shadow reads, compare results, then shift a bounded fraction of traffic. Select a mismatch threshold and latency budget from the product requirements before cutover. Record who can stop the rollout, how the original read path is restored, and whether any written data prevents immediate rollback.

## Risk decisions
Tie a risk to a failure scenario and observable signal. Give it an owner, mitigation, decision deadline, and residual consequence. A spike should answer a named unknown with a decision; it is not an open-ended research task.
