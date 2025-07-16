# ADR: Implement LangChain pipeline for financial document extraction

## Context
We have decided to integrate Google Document AI OCR with the o4-mini language model via LangChain. The goal is to intelligently extract data from financial PDFs.

## Decision
Add `DocumentAIClient` and `O4MiniClient` classes that wrap `google-cloud-documentai` and `llama-cpp-python`. A helper `create_langchain_pipeline` reads environment variables to build an `AsyncPipeline` using these clients. A new README section documents the required configuration.

## Links
- https://cloud.google.com/document-ai/docs (Document AI overview)
- https://python.langchain.com/docs/integrations/tools/document_ai/ (LangChain Document AI integration)
- https://github.com/abetlen/llama-cpp-python (llama-cpp-python repository)

