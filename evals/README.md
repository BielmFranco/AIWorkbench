# Evaluations

There are 75 v2 development cases with domain fixtures and concrete graders. Selection prompts and outcome tasks have different contracts. Five implementation fixtures execute behavior in child workers; design fixtures combine JSON outcome checks with pending human rubrics.

Run `python scripts/run_evals.py` to validate specifications, or explicitly configure an adapter for bounded trials. See [the methodology](../docs/evaluation-methodology.md) and [adapter protocol](adapters/README.md). Controls in `evals/controls/` exercise grader correctness; they are public development artifacts, not held-out evidence of skill efficacy.
