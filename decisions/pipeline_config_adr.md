# ADR: Introduce PipelineConfig for LangChain pipeline

## Context
The LangChain pipeline currently reads environment variables directly in
`create_langchain_pipeline`. This makes testing harder and scatters
configuration logic. Pydantic's `BaseSettings` offers a structured way to
validate environment variables. Google Document AI and the `llama-cpp-python`
model require several variables to be set correctly.

## Decision
Add a `PipelineConfig` class derived from `BaseSettings` in `config.py`. It
defines `doc_ai_project_id`, `doc_ai_location`, `doc_ai_processor_id`, and
`o4mini_model_path`. The `create_langchain_pipeline` function now accepts an
optional `PipelineConfig` instance and defaults to loading from the
environment. Worker code passes in `PipelineConfig()` when building the real
pipeline.

## Consequences
Centralizes pipeline configuration and simplifies testing by allowing explicit
config objects. Environment variables are still supported via Pydantic.

## Links
- https://docs.pydantic.dev/latest/usage/settings/
- https://cloud.google.com/document-ai/docs
- https://github.com/abetlen/llama-cpp-python
