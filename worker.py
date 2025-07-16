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
from config import PipelineConfig
from database import AsyncSessionLocal, File as DBFile, Extraction

celery_app = Celery(
    "smartbooks",
    broker=os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0"),
)

if os.environ.get("USE_REAL_PIPELINE") == "1":
    pipeline = create_langchain_pipeline(PipelineConfig())
else:
    pipeline = AsyncPipeline(StubOCRClient(), StubLLMClient())


@celery_app.task
def process_file_task(file_id: int) -> None:
    """Run the pipeline and store results in the database."""

    async def run_task() -> None:
        async with AsyncSessionLocal() as session:
            file = await session.get(DBFile, file_id)
            if file is None:
                return
            result = await pipeline.run(file.content)
            session.add(Extraction(file_id=file_id, result_json=result))
            await session.commit()

    asyncio.run(run_task())
