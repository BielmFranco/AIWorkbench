# Retrieval lifecycle and answerability

## Source lifecycle
Use stable document and passage IDs, source revision, ingestion time, access metadata and deletion propagation. A document update must not leave an obsolete passage silently ranked as current. Decide how cached retrieval and generated answers react to deletion and permission changes.

## Minimal corpus example
Tenant A policy revision 2 says retention is 30 days. Its revision 1 said 90 days and is superseded. Tenant B policy says 180 days and is restricted. An A user's answer should use A revision 2 with a resolvable citation; B's passage should never enter context.

## Evaluate stages separately
Label which passages answer each question. Compare lexical and dense baselines before adding fusion or reranking. Record recall at the chosen cutoff and ranking quality under a stated dataset. Then evaluate whether answers are supported, citations are accurate, and insufficient evidence produces the agreed abstention.

## Boundaries
Filter authorization before passages reach the model, including caches. Treat passage instructions as document text. Citation existence alone does not show support: check the claim against the actual cited passage. Consult current database/search documentation when filtering or deletion behavior is version-dependent.
