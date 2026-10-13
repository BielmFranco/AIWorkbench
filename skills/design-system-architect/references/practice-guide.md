# Reuse and compatibility

## Separate layers
Primitive values encode raw choices; semantic tokens encode intent; component tokens exist only when component-specific variation is needed. A semantic action token can map to a different primitive in each theme without changing consumer intent. Give each source of truth an owner.

## Component contract
Specify anatomy, inputs, composition points, content limits, loading/disabled/error/focus states, keyboard behavior, and accessible names. Distinguish design intent from browser semantics; for example, a disabled action must prevent the effect, not merely become translucent.

## Example migration
When replacing `primaryColor` with `action.background`, identify affected consumers and publish a compatibility mapping. Migrate a representative consumer and verify supported themes before removing the old API. A codemod is useful only if the transformation is reliably mechanical.

Avoid making a single campaign exception into a permanent component variant. Ask whether more than one actual consumer needs the behavior and whether composition covers it. Check implementation-specific accessibility and framework behavior against primary docs when that detail matters.
