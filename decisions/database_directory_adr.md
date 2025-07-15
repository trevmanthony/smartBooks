# ADR: Ignore local database directory

## Context
We maintain a local SQLite database for uploaded file records. This file should not be tracked in version control.

## Decision
Store the SQLite database in a `data/` directory and add this path to `.gitignore` so the database is excluded from the repository.

## Links
- https://github.com/github/gitignore/blob/main/Python.gitignore
- https://git-scm.com/docs/gitignore
