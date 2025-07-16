# ADR: Integrate Document AI and o4-mini via LangChain community modules

## Context
An earlier ADR explored options for combining Google Document AI OCR with the
o4-mini language model. We considered direct API calls, using LangChain
community modules, or deploying everything serverlessly. The team prefers a
solution that reuses existing tooling yet avoids excess complexity.

## Decision
We will integrate Google Document AI and the o4-mini LLM through LangChain's
community-supported modules. Specifically we will use
`GoogleDocumentAIWarehouseRetriever` to fetch OCR results and
`LlamaCpp` to run o4-mini with the `llama-cpp-python` bindings. This keeps the
implementation consistent with the rest of our LangChain-based pipeline while
maintaining the flexibility to swap components if needed.

## Links
- https://cloud.google.com/document-ai/docs
- https://python.langchain.com/docs/integrations/tools/document_ai
- https://github.com/abetlen/llama-cpp-python
