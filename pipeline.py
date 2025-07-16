"""Async pipeline for Document AI OCR and o4-mini model."""

from __future__ import annotations

from typing import Protocol


# pylint: disable=too-few-public-methods,unused-argument


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
        return await self.llm.generate(text)


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
