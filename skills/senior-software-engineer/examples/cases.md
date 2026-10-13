# Worked example: webhook idempotency

## Input
The endpoint receives `event_id=e42` twice concurrently. Its public response is `200` with the original receipt. A charge must occur once. The gateway accepts an idempotency key.

## Wrong decision
`if not exists(event_id): charge(); insert(event_id)` separates the check from the claim and permits two charges.

## Better decision
Claim `e42` using an atomic unique insert, call the gateway with key `e42`, and persist the resulting receipt. A duplicate in progress follows the existing endpoint contract; a completed duplicate returns the stored receipt. Recovery queries the gateway using the same key rather than issuing an unrelated charge.

## Expected delivery
A patch at the persistence boundary, a test proving one charge for two synchronized requests, a repeat-response test, and recorded checks. If no gateway fake or service is available, report which failure path remains unverified.
