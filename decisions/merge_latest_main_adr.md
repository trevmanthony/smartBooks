# ADR: Merge latest main into work

## Context
We need to bring the latest changes from `main` into the `work` branch. Git's
merge command integrates histories and may require conflict resolution.

## Decision
Run `git merge main` while on `work` and resolve any conflicts, keeping the
Celery features from `work`.

## Sources
- https://git-scm.com/docs/git-merge
- https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts
