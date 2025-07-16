# ADR: Resolve variable naming conflict in tests

## Context
A merge introduced an inconsistent variable name in `tests/test_dockerignore.py`, leading to confusion and conflict markers. Python's PEP 8 recommends clear, consistent variable naming. Git's branching documentation advises resolving conflicts cleanly to maintain readability.

## Decision
Use the original variable name `expected` in the test to match the main branch and avoid unnecessary churn. This aligns with PEP 8 guidelines and simplifies merges.

## Links
- https://peps.python.org/pep-0008/
- https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging
