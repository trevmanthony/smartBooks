# ADR: Asynchronous pipeline with background tasks

## Context
We previously decided to integrate Document AI and the o4-mini model via
LangChain community modules. Running OCR and LLM inference can take time, so the
API should schedule these operations in the background to remain responsive.

## Decision
Implement an `AsyncPipeline` that accepts asynchronous OCR and LLM clients. The
FastAPI endpoint `/process/{id}` adds `AsyncPipeline.run` to `BackgroundTasks` so
files are processed after the response is sent. Stub clients allow local testing
without external services, and real implementations can be injected later.

## Links
- https://fastapi.tiangolo.com/advanced/background-tasks/
- https://docs.celeryq.dev/en/stable/
- https://python.langchain.com/docs/integrations/llms/llamacpp
