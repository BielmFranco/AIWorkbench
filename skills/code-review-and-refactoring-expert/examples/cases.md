# Worked example: pagination review

## Input
Review a diff that changes `limit = request.limit or 50` to `limit = request.limit or 500`. The public API specifies a default of 50. Do not edit.

## Actionable finding
`[P2] Preserve the documented default page size` — When a client omits `limit`, the changed fallback returns up to 500 items instead of 50. Clients that use the default now receive a larger response and different pagination boundaries. Point to the fallback line and the documented contract.

## Unsupported finding
“This expression is ugly; use a helper.” That is a style preference without demonstrated impact.

## Authorized refactor variant
Extract limit parsing only after verifying omitted, valid, invalid, and boundary inputs. Compare the response and exceptions with the old implementation. A separate bug fix requires its own behavior requirement.
