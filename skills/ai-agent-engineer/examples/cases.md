# Worked example: refund timeout

## Input
An authorized refund call times out. The provider may have issued it. The request key is `acct7:req9`.

## Unsafe recovery
Issue another refund with a fresh key because the first call returned no response.

## Expected transition
Move from requested to unresolved, query `acct7:req9`, and confirm the original refund if present. Retry only using the same key under the provider's documented semantics. Escalate when the bounded recovery cannot confirm state. The ownership check stays in the service.

## Evidence
A local provider fake exercises 'effect happened, response lost', denial and duplicate requests. The ledger contains one refund and the final status is confirmed or explicitly unresolved. A design-only answer proposes these checks and makes no execution claim.
