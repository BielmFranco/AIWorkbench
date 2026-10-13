# Worked example: semantic action tokens

## Input
Two products share button behavior but use different brand colors. Consumers currently read raw palette values.

```json
{"action.background":{"light":"brand.600","dark":"brand.300"},"action.text":{"light":"neutral.0","dark":"neutral.950"}}
```

## Decision
Treat the mapping as illustrative token intent, not a claim that those values meet contrast. Validate actual resolved values in both themes. The component contract includes focus, disabled, pending and keyboard activation.

## Migration
Map the old consumer prop to the semantic role during a deprecation window. Migrate one real consumer, inspect themes and states, and document any unsupported brand mapping before removal.
