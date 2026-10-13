# Worked example: search recovery

## Input
A search page calls an API. Typing a second query can overlap the first. The response may be empty or fail.

## Incorrect behavior
Clearing the query after submission makes retry harder. Accepting the older response last can display results for the wrong query. A spinner replacing the failed state leaves no recovery.

## Expected behavior
Keep the query, tie results to the current request, show an empty-result message distinct from failure, and offer retry after failure. The submit control has a label and keyboard activation. Status feedback is announced without stealing focus while typing.

## Evidence
Run the flow with keyboard, delay the first query behind the second, fail a request, retry, and inspect long result titles at a narrow width. Record unavailable checks explicitly.
