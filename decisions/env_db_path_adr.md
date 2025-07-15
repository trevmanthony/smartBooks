# ADR: Parameterize SQLite database path

## Context
The application previously stored its SQLite file at a fixed path `data/database.db`.
Different deployments may need to place this file elsewhere.

## Decision
Read the database path from the `DB_PATH` environment variable with a default
of `data/database.db`. This allows each deployment to configure storage
without modifying code.

## Links
- https://fastapi.tiangolo.com/advanced/settings/#environment-variables
- https://sqlite.org/whentouse.html
