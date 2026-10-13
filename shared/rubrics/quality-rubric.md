# Quality rubric

Apply only dimensions relevant to the task; mark others N/A. Score an observed deliverable with evidence, not the number of files or headings in a skill.

## Level anchors

| Level | Meaning |
| --- | --- |
| 0 | Missing, unusable, or contradicts an essential requirement; includes false evidence or an unauthorized consequential action. |
| 1 | Names the concern but makes unsupported decisions or omits the required mechanism. |
| 2 | Plausible partial result with a material acceptance gap or an untested assumption presented too confidently. |
| 3 | Meets the task's observable criteria, respects scope, and clearly identifies unverified parts. |
| 4 | Meets level 3 across representative alternatives and relevant failure cases, with reproducible evidence and an appropriate cost. |

## Evidence by dimension

| Dimension | What supports level 3 | What can support level 4 |
| --- | --- | --- |
| Correctness | Task criteria checked against fixtures or supplied evidence | Valid alternative and edge outcomes exercised |
| Selection | Resource-use evidence on relevant and adjacent prompts | Repeated selection trials under a fixed catalog |
| Workflow | Decisions produce the requested artifact without scope drift | Observed recovery on relevant partial failures |
| Specificity | Instructions resolve a real domain decision | Different realistic scenarios handled coherently |
| Recovery | Necessary blocker distinguished from a disclosed limitation | Failure and resumption paths exercised |
| Security | Relevant authority enforced at the correct boundary | Allowed/denied and injected-data paths tested |
| Verifiability | Checks, results and gaps are identified accurately | Reproduction and grader controls available |
| Context efficiency | Only task-relevant resources loaded | Equivalent outcome with measured lower cost |
| Compatibility | Public format and target environment verified | Installation, package and consumer behavior exercised |
| Examples | Input, decision, output and verification are concrete | Examples generalize to held-out task variants |

## Release interpretation

Critical scope, authority and evidence failures block the affected release even when other dimensions score highly. Define task-specific success and acceptable cost before trials. A static review can score document clarity, but it cannot score behavioral efficacy. Report reviewer, task, evidence and uncertainty with every score. Do not claim level 4 from an unexecuted plan or average away a critical failure.
