# ADR: Plan integrating Google Document AI OCR and o4-mini via LangChain

## Context
We want to add OCR capabilities using Google Document AI and leverage the o4-mini language model through LangChain. This will let the app extract text from scanned PDFs and process it with a lightweight LLM.

## Sources
- <https://cloud.google.com/document-ai/docs>
- <https://github.com/langchain-ai/langchain/blob/master/libs/langchain/langchain/retrievers/google_cloud_documentai_warehouse.py>
- <https://huggingface.co/TheBloke/o4-mini-3B-GGUF>

## Options
1. **Direct API calls**
   - Use the Google Document AI REST API and integrate responses with LangChain's loaders manually. Deploy o4-mini locally via `llama-cpp` and connect using LangChain's LLM interface.
   - *Pros:* Full control over requests; minimal new dependencies.
   - *Cons:* Requires custom auth handling and error management.
2. **LangChain community modules**
   - Utilize LangChain's `GoogleDocumentAIWarehouseRetriever` and `LlamaCpp` classes for o4-mini. Wrap them in custom chains for OCR then text processing.
   - *Pros:* Reuses existing abstractions; easier to extend with other modules.
   - *Cons:* Community modules may change; requires careful version pinning.
3. **Serverless processing**
   - Offload OCR to a Cloud Function invoking Document AI and run o4-mini via an external service, returning results to our app.
   - *Pros:* Less load on our server; scalable.
   - *Cons:* Adds latency and external dependencies.

No final decision is made yet; these options will be evaluated further.
