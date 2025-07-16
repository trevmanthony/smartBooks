"""Async database models and helpers."""

from __future__ import annotations

import asyncio
from typing import Optional

from sqlalchemy import Column, LargeBinary, Text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Field
from sqlmodel.ext.asyncio.session import AsyncSession

from config import settings

DB_URL = f"sqlite+aiosqlite:///{settings.db_path}"
engine = create_async_engine(DB_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class File(SQLModel, table=True):
    """Stored upload record."""

    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    content: bytes = Field(sa_column=Column(LargeBinary))


class Extraction(SQLModel, table=True):
    """Processed pipeline output."""

    id: Optional[int] = Field(default=None, primary_key=True)
    file_id: int = Field(foreign_key="file.id")
    result_json: str = Field(sa_column=Column(Text))


async def init_db_async() -> None:
    """Create all database tables asynchronously."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


def init_db() -> None:
    """Synchronously initialize the database."""
    asyncio.run(init_db_async())
