# ADR: Evaluate LLM integration frameworks

## Context
We considered how to integrate large language model (LLM) features into the smartBooks project. The main options are LangChain, LlamaIndex, or building a custom solution using raw API calls. Recent community discussions highlight both frameworks' growing ecosystems, while articles show how lightweight custom stacks can suffice for small projects.

## Decision
For now we will build a minimal, custom integration without adopting LangChain or LlamaIndex. The project does not yet require advanced chaining or indexing features, and avoiding a heavy framework keeps dependencies small. We may revisit frameworks if our needs grow.

## Links
- https://python.langchain.com/docs/get_started/introduction
- https://docs.llamaindex.ai/en/stable/
- https://platform.openai.com/docs/introduction
- https://www.latent.space/p/build-your-own-rag-stack
