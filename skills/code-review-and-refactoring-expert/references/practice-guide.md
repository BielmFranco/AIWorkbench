# Review and refactor modes

## Review-only
Read the complete relevant change and trace contracts through callers. A defect must have a concrete path to an incorrect outcome. Prioritize changed behavior, security exposure, failure recovery, and measured performance impact. Explain uncertainty when a runtime assumption is not established.

Use severity based on affected users and triggering conditions, not personal style. A clear finding identifies a small code location, the condition that triggers the issue, the observable consequence, and a suggested direction. Avoid asserting that a problem is introduced by a patch without checking the base.

## Behavior-preserving refactor
Identify response shapes, exceptions, ordering, side effects, and persisted values consumers rely on. Characterize that boundary before changing structure. Move one responsibility at a time and use the same acceptance checks after the move. When a bug is discovered during a refactor, document it separately unless fixing it is already in scope.

## Difficult cases
No tests does not automatically mean a defect; explain the uncovered risk. A performance preference without workload evidence is a hypothesis. A public contract break is relevant even if internal tests pass. When the base cannot be obtained, review available code and label what cannot be attributed to the patch.
