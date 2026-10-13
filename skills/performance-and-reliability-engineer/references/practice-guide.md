# Measurement and reliability protocol

## Establish comparable conditions
Record environment, data size, traffic shape, concurrency, warm-up, sample count and measurement window. Include error rate and resource consumption with relevant percentiles. Percentiles from a tiny sample or different load cannot establish a stable improvement.

## Diagnose before changing
Trace the user path and identify the dominant contributor. Make a falsifiable hypothesis and alter one relevant mechanism at a time where practical. A microbenchmark gain does not imply the user path improved. Caching can reduce latency while worsening freshness or tenant isolation; verify those contracts too.

## Sample result
Under the same 200-request fixture, p95 falls from 420 to 180 ms while error rate remains zero and CPU rises within the agreed budget. This supports a measured improvement for that fixture only. If data size or concurrency changed, redo the comparison before attributing the gain.

## Failure behavior
Exercise saturation, timeout and recovery where the service obligation requires them. Bound queues and concurrency rather than hiding overload behind retries. Record recovery time and correctness under failure, then choose a regression signal linked to the actual bottleneck.
