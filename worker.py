"""Celery worker entrypoint for the document pipeline."""

import os
import asyncio
from celery import Celery
from pipeline import (
    AsyncPipeline,
    StubOCRClient,
    StubLLMClient,
    create_langchain_pipeline,
)

celery_app = Celery(
    "smartbooks",
    broker=os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0"),
)

if os.environ.get("USE_REAL_PIPELINE") == "1":
    pipeline = create_langchain_pipeline()
else:
    pipeline = AsyncPipeline(StubOCRClient(), StubLLMClient())


@celery_app.task
def process_file_task(data: bytes) -> str:
    """Run the OCR+LLM pipeline inside Celery."""
    return asyncio.run(pipeline.run(data))
