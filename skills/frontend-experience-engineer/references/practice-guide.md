# Interaction implementation

## Specify transitions
For each action define event, pending state, success state, failed state, feedback, and focus destination. Keep editable input and recovery available after a failed request. Prevent a stale response from replacing the result of a newer query using cancellation or a request identity check.

## Keyboard and semantics
Prefer native controls when their semantics match. Provide a persistent accessible label, a visible focus state, and feedback that does not rely on color alone. Decide where focus belongs after a dialog closes or a submitted form succeeds. Announce meaningful asynchronous changes without making every keystroke noisy.

## Verify the flow
Use the repository's browser tools when available. Inspect the actual page before choosing element references, refresh after significant DOM changes, and capture relevant evidence. Exercise slow and failed responses, long text, and a narrow viewport. Follow the product's support targets rather than inventing a universal device matrix.

Performance decisions need user-path evidence. Do not introduce memoization or bundle changes merely because a pattern exists in a guide. Read framework-specific primary documentation when the installed version affects an implementation.
