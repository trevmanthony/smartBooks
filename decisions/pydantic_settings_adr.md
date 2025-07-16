# ADR: Adopt Pydantic Settings

## Context
Configuration values were previously read in `app.py` using `os.getenv`.
Pydantic's `BaseSettings` provides validation and automatic environment
parsing. FastAPI's documentation recommends this approach for managing
configuration.

## Decision
Introduce a `config.py` module defining a `Settings` class derived from
`pydantic_settings.BaseSettings`. Instantiate a single `settings` object and
import it in `app.py` to access `db_path` and `max_file_size` fields.
Environment variables `DB_PATH` and `MAX_FILE_SIZE` now override the defaults.

## Links
- https://docs.pydantic.dev/latest/usage/pydantic_settings/
- https://fastapi.tiangolo.com/advanced/settings/
