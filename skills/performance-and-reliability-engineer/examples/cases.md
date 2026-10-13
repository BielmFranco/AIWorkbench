# Worked example: API regression

## Protocol
Fixed dataset, 200 requests, equal concurrency and environment, equal warm-up. Record p50/p95/p99, errors, CPU and memory before and after an index change.

## Hypothesis
The query plan scans rows that an index can narrow. Confirm with the actual query plan and trace.

## Valid conclusion
If p95 improves under matched load and correctness checks hold, report the measured result with sample and resource cost. Compare several runs when variance is large.

## Invalid conclusion
'The API is twice as fast' based on a single local query, or an after-run with fewer requests. Preserve the raw measurements and limit the claim to the measured workload.
