# ADR: Inject database path via FastAPI dependency

## Context
The application used a module-level `DB_PATH` constant, requiring module reloads in tests to use a temporary database. This made tests slower and harder to maintain.

## Decision
Implement a `get_db_path` dependency returning `app.state.db_path`. Each route receives `db_path: str = Depends(get_db_path)` and `init_db` accepts the path as a parameter. Tests override `get_db_path` to point to a temporary file, avoiding module reloads.

## Links
- https://fastapi.tiangolo.com/tutorial/dependencies/
- https://docs.pytest.org/en/latest/how-to/tmp_path.html
