# ADR: Merge main into work branch

## Context
The `work` branch had diverged from `main` and needed updates from the latest `main` commits. Git's merge operation integrates changes from another branch while preserving each commit's history.

## Decision
Run `git merge main` while on the `work` branch and resolve any conflicts, keeping the Celery implementation and new tests from `main`. Follow Git's merge workflow as described in the official documentation.

## Sources
- <https://git-scm.com/docs/git-merge>
- <https://www.atlassian.com/git/tutorials/using-branches/git-merge>
