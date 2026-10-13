# Evaluations that distinguish correct outcomes

## Specify one task precisely
Provide input artifacts, starting state, allowed actions, requested output and observable success. A design answer and an executed implementation need different criteria. A test that recognizes headings cannot establish task success.

## Grader controls
For a numeric result, check the value and provenance rather than wording. For code, execute behavior against relevant fixtures. For judgment, anchor rubric levels with examples and calibrate to blinded human labels. Include a correct alternative path, an incomplete answer and a plausible wrong answer to test the grader itself.

## Paired trial
Keep baseline and candidate inputs, model, tools, permissions and budgets equivalent. Isolate workspaces and prevent the baseline from loading candidate skills. Record version/hash, time, usage if available, process outcome, trace and artifact verdicts. Repeat variable cases and inspect failures before revising instructions.

## Release decision
Keep critical safety failures separate from average quality. Report a small sample as a small sample, do not infer a broad confidence claim from one success. Hold out tasks used to assess generalization; tests used to tune a prompt are not held out.
