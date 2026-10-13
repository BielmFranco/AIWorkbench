# Support refund assistant: design and failure-test plan

## Outcome and baseline

Use a deterministic refund service. The assistant interprets the account owner's explicit request, collects an unambiguous charge identifier, invokes the service, and reports its recorded outcome. The service owns authorization, state transitions, provider calls, retry decisions, and escalation. Autonomous tool selection, durable model memory, and multiple agents are unnecessary for this workflow.

The requested operation is a refund of the identified charge under the product's refund policy. If the charge or refund scope is ambiguous, ask for that missing detail before submitting. An authenticated owner's explicit request is authorization for the requested refund; do not introduce an extra confirmation step. Authentication alone is not evidence that the owner requested a refund.

Success means an authoritative provider lookup for the original request key confirms the refund and its association with the intended charge, and that evidence is persisted in the service's operation record. An assistant's statement or the refund response alone does not establish completion. A terminal denial is a resolved, unsuccessful outcome. Pending or unknown effects are unresolved.

## Contracts and authority

The schemas below are proposed service contracts, not claims about the provider's undocumented response format. Validate inputs with strict object schemas (no unknown properties), nonempty bounded strings, enums, and status-specific required fields. Validate provider responses before assigning a state.

| Capability | Input and output | Authority and effect | Timeout and recovery |
| --- | --- | --- | --- |
| Assistant-facing `request_refund` | Input: `{charge_id: string, client_request_id: string}`. Output: `{operation_id: string, status: confirmed\|denied\|unresolved\|needs_details, refund_id: string\|null, reason_code: string\|null}`. Confirmed requires a refund ID and persisted verification evidence. | Server derives account identity from the authenticated session; accepts no model-supplied account identity. It verifies explicit request scope, charge ownership and refund eligibility before mutation. This capability may change the provider ledger. | Service budget below. Returns persisted status and a tracking reference even if recovery is unresolved. A caller disconnect does not reset the operation. |
| Provider adapter `refund` | Provider input exactly `(charge_id, request_key)`. Proposed normalized output: `{status: accepted\|confirmed\|denied\|unknown, refund_id: string\|null, reason_code: string\|null}`. Invalid, incomplete, or unmappable responses become unknown. | Service-only credentials. Request key is service-generated and durably bound to one account, charge and logical operation. State-changing; retry safety is conditional on documented provider semantics. | Ten-second attempt timeout, including SDK retries (disable hidden SDK retries). A timeout, malformed response, interrupted connection, or ambiguous error moves the operation to unresolved and triggers lookup. |
| Provider adapter `lookup` | Provider input exactly `(request_key)`. Required normalized output: `{status: confirmed\|denied\|pending\|not_found\|unknown, refund_id: string\|null, charge_id: string\|null, reason_code: string\|null}`. Confirmed must provide trustworthy charge association, directly or through a documented immutable key binding. | Service-only read. No financial side effect. Provider status is evidence only after response validation. | Ten-second attempt timeout. Timeout, mismatch, eventual-consistency uncertainty, and unknown response remain unresolved. Retry within the shared budget. |

Confirm before rollout: refund deduplication semantics, key retention duration, binding of a key to its original charge, lookup authority and consistency, meanings of terminal outcomes, and whether cancellation/timeouts stop server processing. The existence of `request_key` does not prove idempotency. If lookup cannot authoritatively verify the effect, automated completion is unavailable; preserve the operation for human reconciliation.

Default to at most one refund invocation while these semantics are unverified. Enable a second same-key invocation only when documented guarantees prevent a second effect despite a concurrent or late first invocation, and the retry remains inside the key's retention window. A not-found lookup alone does not authorize retry: an in-flight call or eventual consistency may still conceal the first effect.

## Durable state and transitions

Persist an operation record before making any provider call: operation ID, derived owner ID, charge ID, requested scope, stable request key, explicit-request evidence, authorization decision, current status, timestamps/deadline, reserved attempt counters, provider evidence and escalation reference. Persist state updates and attempt reservations transactionally. Restrict sensitive audit data and avoid storing credentials.

Deduplicate `(authenticated_account_id, client_request_id)` and reject reuse with a different charge or scope. Return the existing operation for repeated requests. Use a per-charge lock or equivalent database constraint to serialize refund decisions, check already refunded amounts, and prevent a second operation while an earlier refund remains unresolved. A repeated chat request must resolve to the existing operation where possible; a new client ID is not permission to refund the same charge again. If ownership or eligibility cannot be established, make no mutation.

1. **Proposed -> authorized or denied:** service authenticates the caller, checks charge ownership, request scope and eligibility. Invalid or ambiguous scope becomes needs_details. Failed authorization is denied with zero provider mutations.
2. **Authorized -> requested:** persist request key and reserve the attempt before sending `refund`. Recheck authorization before any later mutation. Send the stable key, never a fresh recovery key.
3. **Requested -> verifying/unresolved:** even a positive refund response needs lookup verification. A timeout or crash is ambiguous: the effect may have occurred. On restart, reconcile the persisted key before considering another mutation.
4. **Lookup -> confirmed:** validated authoritative evidence identifies the original operation's refund and charge. Persist evidence and terminal status; subsequent calls return it without mutation.
5. **Lookup -> denied:** only authoritative terminal evidence establishing no refund and no pending effect permits denial. A retryable rejection or uncertain refund response is not such evidence.
6. **Lookup -> unresolved:** pending, uncertain not_found, timeout, invalid response or mismatched charge never become success or failure by inference. Perform only bounded recovery. A second mutation is optional only after lookup and the documented safety conditions above; otherwise continue read-only reconciliation.
7. **Budget exhausted -> escalated unresolved:** atomically persist a handoff for human reconciliation and return the tracking reference. Do not restart the budget on a duplicate request, worker restart, or assistant rephrasing.

Use one worker lease with fencing or equivalent serialized ownership for each operation. Persist attempt reservations before dispatch so a crash can consume an attempt without exceeding the cap. Provider timeouts may leave processing in flight; client-side serialization is not a substitute for provider deduplication. Without safe replay guarantees, a crash between reservation and dispatch still causes reconciliation and possible escalation rather than a speculative new mutation.

## Attempts, duration and escalation

Set a 60-second automatic recovery deadline from the first attempt reservation. At most two refund invocations, at most three lookup invocations, and at most five provider invocations total per logical operation. Without verified safe replay, the bound is one refund plus three lookups, four total. Reserve enough lookup budget to verify any second mutation; if no lookup remains, do not send it.

All calls are serial, each capped at ten seconds. Use at most two backoff waits, one second then three seconds; honor a longer provider retry-after only if another full attempt fits before the deadline. Check remaining time before dispatch. Stop earlier when the outcome is terminal or recovery is unsafe. The maximum configured call and wait time is 54 seconds; the 60-second deadline also bounds scheduling and local processing. Local deadline expiry records unresolved and escalates even if a provider call might complete later. These are invocation bounds, not a claim that the provider stops processing at the deadline.

Escalate when confirmation is still unavailable, status conflicts, a safety precondition is missing, or the deadline/attempt cap is reached. The handoff contains operation and charge references, original key, authorization evidence, attempts and their times, last lookup evidence and the reason recovery stopped. Tell the user: “The refund status is unresolved. Your reference is [operation ID]; support will reconcile it.” Never say that no refund occurred merely because a response timed out.

Human support reconciles using the same key and authoritative provider records before any financial action. Handoff is not authorization to issue a fresh-key refund. Further automated work must not silently reset this operation's attempt cap. A late confirmed result may update the existing record with validated evidence and close the escalation; it must not initiate another mutation. Escalation delivery is proposed in this design, not performed here.

## Failure-test plan

Use a deterministic provider fake with separate controls for ledger effect, response delivery, lookup consistency and delayed processing; use a fake clock and persistent operation store. Independently inspect the fake ledger and persisted state, rather than grading assistant prose. The principal invariant is at most one financial refund for an authorized logical operation, and zero for unauthorized requests; confirmed requires matching authoritative evidence. The safe-replay configuration must fail closed if its guarantees are absent.

| Scenario | Injected behavior | Expected assertions |
| --- | --- | --- |
| Normal success | Refund succeeds; lookup confirms matching charge/refund. | One financial effect; status confirmed with evidence; no unnecessary retry. |
| Ownership/authentication denial | Wrong owner, expired session, model-supplied owner claim, or failed ownership read. | Zero mutations; denied or unresolved authorization check as appropriate; identity derived only by server. |
| Missing request details | Ambiguous charge or scope, or no explicit refund request. | needs_details; zero mutations. |
| Terminal provider denial | Authoritative lookup proves denial with no pending effect. | Denied; no refund effect; no repeated mutation. |
| Effect occurred, response lost | Refund commits then times out. | Lookup original key confirms; exactly one effect; no fresh key. |
| No effect, response lost | Refund does not commit and response times out. | Reconcile first; same-key replay only under documented safe guarantees; otherwise unresolved escalation. |
| Lookup is temporarily not_found | First refund remains in flight or lookup is eventually consistent. | No assumption of failure; no unsafe replay; delayed commit cannot cause duplicate effect. |
| Safe same-key replay | Verified idempotent provider; first result unknown; allowed retry. | Two mutation invocations maximum, same key and charge, at most one effect; later lookup verifies. |
| No replay contract | Provider has a key but deduplication behavior/retention is unknown. | At most one refund invocation; unresolved escalation if lookup cannot resolve. |
| Repeated and concurrent requests | Same ID, conflicting reuse, multiple IDs for same charge, and concurrent workers. | Existing operation returned or conflicting request rejected; charge serialization prevents duplicate refund; counters do not reset. |
| Crash/restart | Crash before dispatch, after dispatch, after response, and before evidence persistence. | Durable key survives; reserved attempts count; reconcile before any further mutation; preserve caps across restart. |
| Lookup failures/pending | Three lookups time out or remain pending. | Unresolved; persisted handoff; attempt and duration bounds obeyed. |
| Corrupt or conflicting responses | Unknown enum, missing refund ID, wrong charge, inconsistent terminal status. | No false confirmation; unresolved with diagnostic evidence and escalation. |
| Late completion after escalation | Provider commits after local deadline. | Existing operation can reconcile to confirmed with matching evidence; no new mutation. |
| Authorization changes before retry | Ownership/eligibility changes after first attempt. | No further mutation; original potential effect remains subject to reconciliation. |
| Retry and deadline boundaries | Hidden SDK retry, retry-after beyond deadline, exhausted lookup quota, repeated reconnects. | SDK retries disabled; no new call without full remaining time; max two refund/three lookup/five total (or four without safe replay); deadline never resets. |
| Retrieval/tool injection | Charge description or provider text tells assistant to change identity, key, or retry policy. | Treated as data; server ignores such instructions and enforces schema/authorization. |
| Already refunded charge | Prior terminal refund or unresolved earlier operation exists. | Return prior result or route to its reconciliation; no excessive cumulative refund. |

Record invocation counts, final ledger effects, terminal evidence, unresolved handoff completeness, simulated elapsed time, and trace consistency for each trial. Acceptance requires every invariant to hold, including lost-response and crash cases. Provider integration tests later must validate real idempotency, lookup consistency, and key retention before enabling replay.

## Evidence and limitations

This deliverable is a design review of success, denial, duplicate, crash, timeout and escalation transitions. No runtime implementation, provider call, ledger verification, or failure trial was executed. The key missing evidence is the provider's documented replay and lookup semantics; the conservative one-mutation design remains valid while those are unknown.

The skill and its worked refund example were consistent and did not cause confusion. Its explicit minimal-autonomy instruction led to a deterministic service with the assistant restricted to interpretation and communication; its bounded recovery and original-key requirements shaped the retry design.
