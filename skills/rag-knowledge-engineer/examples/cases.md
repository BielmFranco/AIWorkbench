# Worked example: tenant policy

## Fixture
`A/policy@2`: retention 30 days, authorized and current. `A/policy@1`: 90 days, obsolete. `B/policy@1`: 180 days, forbidden for A. A removed appendix has no searchable content.

## Expected answer
For A's retention question: 30 days, citing the passage from `A/policy@2`. For a question answered only by the removed appendix: insufficient evidence according to the product policy.

## Failure to detect
Returning the 180-day policy, citing a passage the model never saw, or exposing B's text in a trace even when the final answer abstains.

## Evidence
Test retrieval IDs and model context separately from final answer/citation correctness. Repeat after a revision, ACL change and deletion, including cached queries.
