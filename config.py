"""Application settings module."""

from __future__ import annotations

from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration values loaded from the environment."""

    db_path: Path = Path(__file__).with_name("data").joinpath("database.db")
    max_file_size: int = 16 * 1024 * 1024


settings = Settings()
