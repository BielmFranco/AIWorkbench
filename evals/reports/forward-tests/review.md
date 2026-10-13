# Pagination patch review

Review-only; no code changes made.

Public contract: omitting `limit` defaults to 50; explicit positive limits remain accepted.

Base:
```python
def page(limit=None):
    size = limit or 50
    return size
```

Candidate:
```python
def page(limit=None):
    size = limit or 500
    return size
```

## Finding

**[P2] Preserve the contracted default of 50**

Location: candidate line 2, `size = limit or 500`.

When a caller invokes `page()` (or `page(None)`), `limit` is `None`, so the candidate returns 500. The base returns 50, as required by the supplied public contract. This changes the default page size by a factor of ten and breaks callers relying on the promised default. Restore the fallback to 50.

Explicit positive limits still pass through unchanged in both versions: for any positive `n`, `page(n)` returns `n`. No finding is justified for that contract requirement.

## Evidence and scope

The result follows directly from evaluating the supplied expressions: `None or 50` is 50, `None or 500` is 500, and positive values are truthy. No runtime tests were run; these conclusions use the complete supplied snippets. No repository callers or additional contracts were assumed. Behavior for zero, negative values, and other input types is outside the supplied contract and was not reported as a defect.

Read the requested skill, its practice guide, and its pagination worked example. No confusing instructions were found. No catalog files were changed.
