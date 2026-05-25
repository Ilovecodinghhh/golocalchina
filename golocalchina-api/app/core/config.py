"""Application configuration — env-driven via pydantic-settings."""
import os
import secrets
import warnings
from pydantic_settings import BaseSettings

# Default DB: SQLite for local dev, PostgreSQL for Railway (set DATABASE_URL env var)
_default_db = "sqlite+aiosqlite:///./golocalchina.db"
if os.environ.get("RAILWAY_ENVIRONMENT"):
    _default_db = os.environ.get("DATABASE_URL", "sqlite+aiosqlite:////tmp/golocalchina.db")
    # Railway PostgreSQL URLs use postgres:// but asyncpg needs postgresql+asyncpg://
    if _default_db.startswith("postgres://"):
        _default_db = _default_db.replace("postgres://", "postgresql+asyncpg://", 1)
    elif _default_db.startswith("postgresql://"):
        _default_db = _default_db.replace("postgresql://", "postgresql+asyncpg://", 1)

# Generate a random JWT secret if none is provided (warn loudly)
_default_jwt_secret = os.environ.get("JWT_SECRET_KEY", "")
if not _default_jwt_secret:
    _default_jwt_secret = secrets.token_urlsafe(64)
    warnings.warn(
        "JWT_SECRET_KEY not set! Generated a random one. "
        "Tokens will be invalidated on restart. Set JWT_SECRET_KEY in environment.",
        stacklevel=1,
    )


class Settings(BaseSettings):
    database_url: str = _default_db
    jwt_secret_key: str = _default_jwt_secret
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7
    platform_name: str = "GoLocalChina"
    cors_origins: str = "https://golocalchina.vercel.app,http://localhost:3000"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
