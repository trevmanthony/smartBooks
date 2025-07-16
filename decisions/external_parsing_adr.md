# ADR: Offload Parsing to External Services

## Context
The application must extract text from uploaded documents and analyze that text for financial insights. Running accurate optical character recognition (OCR) and large language model (LLM) reasoning locally would require significant compute and maintenance overhead.

## Decision
OCR is delegated to Google Cloud Document AI, which provides scalable, high‑quality extraction for PDFs and images. The recognized text is then sent to the OpenAI `o4-mini` model to generate insights. Using managed APIs keeps server requirements minimal while leveraging state-of-the-art models.

## Links
- https://cloud.google.com/document-ai/docs/overview
- https://platform.openai.com/docs/models/gpt-4o
