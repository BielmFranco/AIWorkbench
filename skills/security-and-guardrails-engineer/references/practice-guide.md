# Evidence-led security work

## Define the threat
Identify asset, attacker capability, entry point and the boundary being crossed. A model receiving hostile text is an exposure; a vulnerability claim needs a path to an unauthorized outcome. Distinguish confirmed findings, plausible hypotheses and missing evidence.

## Authorization example
A refund endpoint must derive permission from the authenticated principal and the charge owner, not from the account ID supplied by the caller or an assistant's assertion. Deny a cross-account attempt before the ledger write. Logging should record the denied action without storing the raw secret or full sensitive payload.

## AI tool boundary
Retrieved instructions remain data. Prompts can help behavior, but hard permissions, resource restrictions and transaction limits belong in services or infrastructure. Test a legitimate request and the corresponding denied request using controlled fixtures. Include hostile tool content when it is relevant to the boundary.

## Recovery and scope
Use least privilege and a concrete containment/recovery plan proportional to the asset. Continue read-only analysis when runtime access is unavailable. Treat live scans, credential use and state-changing security tests as actions that need authorization for that environment.
