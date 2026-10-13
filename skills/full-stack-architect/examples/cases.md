# Worked ADR: order notification

## Context
An order can be charged successfully while notification delivery fails. Repeating the charge is unacceptable. Notification may be delayed for up to the agreed recovery window.

## Decision
Persist payment outcome and notification intent in the owning service. A dispatcher retries notification using an event ID; the order consumer deduplicates it. Reconciliation identifies old undelivered events.

## Alternatives and tradeoff
A synchronous call is simpler but makes order recovery depend on a partial network failure. The outbox adds a dispatcher, delay, and operational ownership. It does not make arbitrary cross-service transactions atomic.

## Evidence to obtain
Crash after persistence, duplicate dispatch, unauthorized order access, and recovery-window monitoring. Size queue and storage from a stated arrival-rate assumption, then measure.
