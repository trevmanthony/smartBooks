# ADR: Adopt LangChain for LLM integration

## Context
The earlier [llm_framework_adr.md](llm_framework_adr.md) concluded that our project did not yet need a framework like LangChain or LlamaIndex. Since then both the Google Document AI module and LlamaCpp bindings have matured. LangChain's 0.1.0 release highlights improved stability and integrations, making it easier to combine OCR and local models.

## Decision
We will adopt LangChain as the primary framework for our LLM workflows. Its built-in `GoogleDocumentAIWarehouseRetriever` and `LlamaCpp` integrations let us reuse community-tested modules while keeping the option to swap components later. A follow-up task will implement the new pipeline using these features.

## Links
- https://blog.langchain.com/langchain-v0-1-0/
- https://python.langchain.com/docs/integrations/tools/document_ai/
- https://github.com/abetlen/llama-cpp-python
