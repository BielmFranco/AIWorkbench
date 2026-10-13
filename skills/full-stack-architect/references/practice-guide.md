# Architecture decisions and failure flows

## Select boundaries from obligations
Map who owns data, authorizes changes, and can recover failed operations. Begin with the existing topology and the simplest candidate that satisfies workload and organizational constraints. Distribution adds latency, partial failure, and consistency work; justify it with requirements rather than a diagram style.

## Payment-to-order example
Payment success and order notification are separate facts. If the payment succeeds but the process stops before notification, blindly repeating the payment is unsafe. Record payment status in its owning boundary and use an outbox or reconciliation process for notification. Consumers should handle duplicate events using a stable event ID.

Choose an outbox only where atomic local persistence and event intent are actually needed. State who retries, the maximum recovery delay, monitoring signals, and how an unresolved event is escalated.

## Decision record
For each costly choice include requirement, alternatives, chosen mechanism, tradeoff, reversal cost, and the signal that would warrant revisiting it. Model tenant isolation and access checks at data and API boundaries when applicable. Verify installed dependency behavior against its current official documentation when making version-specific choices.
