# ADR: Display extraction results in the UI

## Context
The pipeline processes uploaded financial documents using Google Document AI and the o4-mini model. Currently results are only returned from the Celery task. We want to show the structured data in the web UI after processing.

## Decision
Add an endpoint that retrieves the processed JSON from the pipeline and renders it in a template. Use LangChain output parsers to ensure consistent JSON structure.

## Links
- https://cloud.google.com/document-ai/docs/processors-list#processor_invoice-processor
- https://python.langchain.com/docs/modules/model_io/output_parsers/
