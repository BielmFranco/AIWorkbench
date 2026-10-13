# Worked finding: cross-account refund

## Evidence
The caller is authenticated as account A, but the endpoint trusts a payload naming account B and writes a refund without checking the charge's owner.

## Impact and condition
A caller who knows B's charge ID can change B's ledger. Point to the missing ownership check and the reachable write, rather than reporting 'input validation is weak'.

## Control and check
Look up the charge owner server-side, compare it with authenticated authority and deny before mutation. Test A-to-A allowed and A-to-B denied. Assert that the denied request writes no refund and logs no secret.

## Scope limit
This controlled fixture supports the finding. It does not authorize trying the exploit on a live customer account.
