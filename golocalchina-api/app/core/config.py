"""Application configuration — env-driven via pydantic-settings.

Merged from golocalchina-backend:
- Supports both SQLite (dev/demo) and PostgreSQL (production)
- Environment-based database URL selection
- Redis support for caching
- Structured logging configuration
"""
import os
from typing import Literal

from pydantic_settings import BaseSettings


def _default_db_url() -> str:
    """Return appropriate default DB URL based on environment."""
    if os.environ.get("RAILWAY_ENVIRONMENT"):
        return "sqlite+aiosqlite:////tmp/golocalchina.db"
    return "sqlite+aiosqlite:///./golocalchina.db"


class Settings(BaseSettings):
    # Runtime
    env: Literal["dev", "staging", "prod"] = "dev"
    debug: bool = False
    
    # Database
    database_url: str = _default_db_url()
    
    # Redis (optional, for caching)
    redis_url: str = ""
    
    # Auth
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7
    
    # Platform
    platform_name: str = "GoLocalChina"
    cors_origins: str = "https://golocalchina.vercel.app,http://localhost:3000"
    
    # Logging
    log_level: str = "INFO"
    log_format: Literal["json", "console"] = "console"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
