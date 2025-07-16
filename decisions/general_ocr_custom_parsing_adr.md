# ADR: General OCR with custom LangChain parsing

## Context
We chose Option 2 from the planning discussion: use Document AI's general OCR processor to extract raw text, then parse financial fields via a custom prompt handled by LangChain and the o4-mini model.

## Decision
Implement a prompt that asks the LLM to extract invoice number, date, and total amount from the OCR text. The `AsyncPipeline.run` method now builds this prompt before passing it to the LLM.

## Links
- https://cloud.google.com/document-ai/docs/overview
- https://python.langchain.com/docs/modules/model_io/prompts/prompt_templates/
