"""Application settings module."""

from __future__ import annotations

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration values loaded from the environment."""

    model_config = SettingsConfigDict(env_file=".env")

    db_path: Path = Path(__file__).with_name("data").joinpath("database.db")
    max_file_size: int = 16 * 1024 * 1024


settings = Settings()


class PipelineConfig(BaseSettings):
    """Settings for the Document AI and o4-mini pipeline."""

    model_config = SettingsConfigDict(env_file=".env")

    doc_ai_project_id: str
    doc_ai_location: str = "us"
    doc_ai_processor_id: str
    o4mini_model_path: str
