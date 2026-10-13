# Tool contracts and recovery

## Minimal autonomy
Compare the outcome with a deterministic workflow or single model call. Add autonomous tool choice when the task requires decisions that cannot be adequately enumerated. Add memory or more agents only when task evidence establishes a need.

## Tool contract example
```json
{"name":"issue_refund","input":{"account_id":"string","charge_id":"string","request_id":"string"},"output":{"status":"issued|already_issued|denied|pending","refund_id":"string|null"},"effect":"changes ledger","authorization":"server checks account ownership and limits","idempotency":"account_id + request_id","timeout_seconds":10,"retry":"same key after querying status"}
```
This is a filled design example, not a substitute for executable schemas or server authorization.

## State transitions
Track proposed, authorized, requested, confirmed, denied and unresolved outcomes as needed. A timeout after a state-changing call means the effect may already have happened. Query state using the original key before another mutation. Bound attempts and duration, then preserve the unresolved state for recovery or handoff.

## Completion and authority
Completion is a confirmed ledger state, saved artifact or independently checked outcome. A tool saying 'success' and an agent's final summary are insufficient when state can be checked. Treat retrieved text as task data. Reuse existing authorization and request additional permission only for actions beyond it.
