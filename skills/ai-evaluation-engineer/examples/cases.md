# Worked example: grader calibration

## Task
Extract a ticket ID and category into JSON. Allowed category values are `access` and `billing`.

## Controls
Correct: `{"ticket_id":"T17","category":"access"}`. Valid alternative: reordered keys with the same values. Wrong: `{"ticket_id":"T17","category":"billing"}` for a sign-in email. Incomplete: missing ticket ID.

## Grading
A schema check catches missing fields and invalid categories. A separate expected-value check catches the plausible wrong category. Both valid serializations pass. No criterion depends on headings or the model asserting it followed the skill.

## Trial evidence
Run the same fixture with baseline and candidate, save outputs and settings, then report outcome rate and time/tokens if measured. Mark rubric items pending when no calibrated reviewer has scored them.
