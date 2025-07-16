"""Async pipeline for Document AI OCR and o4-mini model."""

from __future__ import annotations

# pylint: disable=too-few-public-methods,unused-argument, import-outside-toplevel, broad-exception-caught, useless-import-alias, invalid-name
from typing import Protocol

try:  # optional import for patching in tests
    from google.cloud import (
        documentai as DOCUMENTAI,
    )  # pylint: disable=broad-exception-caught
except Exception:  # pragma: no cover - optional dependency may be missing
    DOCUMENTAI = None  # type: ignore

try:
    from langchain_community.llms.llamacpp import LlamaCpp as LLAMACPP
except (
    Exception
):  # pragma: no cover - optional dependency may be missing  # pylint: disable=broad-exception-caught
    LLAMACPP = None  # type: ignore
# pylint: disable=too-few-public-methods,unused-argument, import-outside-toplevel, broad-exception-caught, useless-import-alias, invalid-name


class OCRClient(Protocol):
    """Protocol for OCR extraction clients."""

    async def extract(self, data: bytes) -> str:
        """Return text extracted from raw file bytes."""


class LLMClient(Protocol):
    """Protocol for language model clients."""

    async def generate(self, prompt: str) -> str:
        """Return an LLM response for the given prompt."""


class AsyncPipeline:
    """Asynchronously process files using OCR and LLM components."""

    def __init__(self, ocr: OCRClient, llm: LLMClient) -> None:
        self.ocr = ocr
        self.llm = llm

    async def run(self, data: bytes) -> str:
        """Run OCR then LLM on the given file bytes."""
        text = await self.ocr.extract(data)
        prompt = (
            "Extract the invoice number, date, and total from this text as JSON.\n"
            f"{text}"
        )
        return await self.llm.generate(prompt)


class StubOCRClient:
    """Simplified OCR client used for tests."""

    async def extract(self, data: bytes) -> str:  # noqa: D401
        """Pretend to extract text from the document."""
        return "stub text"


class StubLLMClient:
    """Simplified LLM client used for tests."""

    async def generate(self, prompt: str) -> str:  # noqa: D401 - simple stub
        """Return a canned response from the LLM."""
        return f"processed: {prompt}"


class DocumentAIClient:
    """OCR client using Google Document AI via the async API."""

    def __init__(self, project_id: str, location: str, processor_id: str) -> None:
        if DOCUMENTAI is None:  # pragma: no cover - handled in tests
            raise ImportError("google-cloud-documentai is required")

        self._client = DOCUMENTAI.DocumentProcessorServiceAsyncClient()
        self._name = self._client.processor_path(project_id, location, processor_id)

    async def extract(self, data: bytes) -> str:  # noqa: D401
        """Send document bytes to Document AI and return extracted text."""
        request = DOCUMENTAI.ProcessRequest(
            name=self._name,
            raw_document=DOCUMENTAI.RawDocument(
                content=data, mime_type="application/pdf"
            ),
        )
        response = await self._client.process_document(request=request)
        return response.document.text


class O4MiniClient:
    """LLM client using llama-cpp-python to run o4-mini."""

    def __init__(self, model_path: str, n_ctx: int = 2048) -> None:
        if LLAMACPP is None:  # pragma: no cover - handled in tests
            raise ImportError("llama-cpp-python is required")

        self._llm = LLAMACPP(model_path=model_path, n_ctx=n_ctx)

    async def generate(self, prompt: str) -> str:  # noqa: D401
        """Run o4-mini on the given prompt asynchronously."""
        import asyncio

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._llm.invoke, prompt)


def create_langchain_pipeline() -> AsyncPipeline:
    """Construct a pipeline using Document AI and o4-mini via LangChain."""
    import os

    project = os.environ.get("DOC_AI_PROJECT_ID")
    location = os.environ.get("DOC_AI_LOCATION", "us")
    processor = os.environ.get("DOC_AI_PROCESSOR_ID")
    model_path = os.environ.get("O4MINI_MODEL_PATH")
    if not (project and processor and model_path):
        raise RuntimeError("Document AI and o4-mini configuration missing")

    ocr_client = DocumentAIClient(project, location, processor)
    llm_client = O4MiniClient(model_path)
    return AsyncPipeline(ocr_client, llm_client)
