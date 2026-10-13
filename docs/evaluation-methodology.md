# Evaluation methodology

The v2 catalog has 75 development cases: three selection prompts and two outcome variants for each of 15 skills. Counts describe current coverage, not a universal sufficiency gate. Selection includes explicit Portuguese, implicit English, and an adjacent negative request. Outcome variants use a domain fixture with and without hostile document text. A design task is graded as a design task; an implementation task must satisfy executable behavior.

## Evidence layers

1. `python scripts/validate.py` checks public metadata and case schemas, version correspondence, fixture paths and grader resources.
2. `python -m unittest discover -s tests -v` exercises format, known correct/wrong artifacts, valid alternatives, grader failures and runner isolation. Controls are harness tests, not model performance.
3. Independent forward tests assess a few realistic requests and record their limitations.
4. Explicit adapter trials run an agent in distinct baseline/candidate workspaces. The runner records artifacts, process traces, elapsed time, available usage, version hashes and checks. Human rubric items stay pending until a reviewer supplies evidence; they are not silently scored by schema checks.

## Setup and bounded execution

```bash
python -m pip install -r requirements-dev.txt
python scripts/run_evals.py
```

The default validates specifications, writes `evals/reports/latest.json`, and reports `not_run` for agent trials. It makes no provider calls.

To run an agent, configure an adapter using [the protocol](../evals/adapters/README.md), then select a small task:

```bash
python scripts/run_evals.py --adapter local-adapter.json --case senior-software-engineer-normal --trials 2 --max-runs 4 --timeout 300
```

Outcome cases run both baseline and candidate; selection runs candidate only. Run directories under `evals/runs/` contain requests, outputs, observations, logs and verdicts. The runner uses command argument lists, not shell-built strings, and bounds provider invocations and process duration. Adapter trials consume provider usage. Simulation adapters are explicitly labeled `simulation` and count as zero live trials.

## Isolation and interpretation

The fixture workspace prevents accidental mixing of generated artifacts. It is not an operating-system security boundary: Python candidates and adapters execute code. Run provider/code trials inside a disposable environment with appropriate filesystem/network restrictions, especially with untrusted artifacts. Child workers separate candidate imports from grader assertions but do not constitute a secure malware sandbox.

The infrastructure is exercised on Python 3.12. Windows process cleanup requires nested job objects (Windows 8 / Server 2012 or newer): child processes are assigned before they resume, and closing the job terminates descendants even after the original parent exits. POSIX execution uses a process group. These are lifetime controls, not complete security containment.

Development controls and examples are public. They are not held-out benchmarks and can be read by a model on the same host. For a quality certification, prepare separate held-out inputs outside the model's readable environment, prevent baseline access to candidate skills and controls, and keep model/tool/settings/permissions/budgets equivalent. Record model identity and dependency versions. Inspect traces for leakage and invalid grading paths before interpreting a gain.

Selection must be based on instrumented resource reads, not final-answer self-report. The bundled Codex adapter retains command-reference hints for human inspection but cannot certify actual selection or absence across every tool; its routing cases remain ungraded. An adapter with complete read instrumentation can score them.

Fix outcome/efficiency gates before trials. Report trial counts and uncertainty, include valid alternative outcomes, and calibrate human judgments against anchored examples. A mean from one small fixture suite is descriptive evidence only. Add failures to regression cases without tuning on the held-out set.
