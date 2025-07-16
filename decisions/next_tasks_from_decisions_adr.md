# ADR: Record Next Tasks from ADR Review

## Context
Reviewing the `decisions` folder revealed several future improvements that were noted but not tracked in `TODO.md`.

## Decision
Add the following tasks to `TODO.md`:

- Introduce `BaseSettings` from Pydantic to validate environment configuration.
- Evaluate using an async-friendly database layer such as SQLModel or SQLAlchemy.
- Choose an integration approach for Google Document AI OCR and the o4-mini LLM.

## Links
- https://docs.pydantic.dev/latest/usage/pydantic_settings/
- https://fastapi.tiangolo.com/advanced/settings/
- https://sqlmodel.tiangolo.com/
- https://docs.sqlalchemy.org/en/20/orm/
- https://cloud.google.com/document-ai/docs
- https://huggingface.co/TheBloke/o4-mini-3B-GGUF
