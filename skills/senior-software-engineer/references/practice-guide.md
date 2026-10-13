# Implementing a compatible change

## Decide the boundary first
Trace the request from its caller to the system of record. Write down the successful result, error result, retry behavior, and public contract. Inspect repository dependencies before choosing an API or importing a library; consult its primary documentation when the installed version matters.

## Example: concurrent webhook delivery
A webhook key must be claimed atomically at the persistence boundary. Checking existence and then inserting in separate operations permits both concurrent requests to pass. A unique constraint or equivalent atomic operation prevents that race. Store the completed result so a repeat can return the documented response. Decide what happens when the process stops after claiming the key but before completing the side effect.

Do not assume that a database transaction makes an external payment call exactly once. Use an external idempotency key or reconciliation when the side effect crosses that boundary.

## Pick discriminating checks
Test one delivery, a completed repeat, concurrent duplicates, and a failure followed by retry when those paths are part of the contract. A test that only checks the new helper's name does not verify the behavior. Use controlled synchronization for concurrency rather than hoping a sleep reproduces the race.

## Finish with evidence
Record relevant commands and actual results, compatibility effects, and unresolved risk. Use a deployment note only when the change affects release or data migration. Keep user-owned edits separate from the requested change.
