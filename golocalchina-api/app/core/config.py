"""Application configuration — env-driven via pydantic-settings."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database — SQLite for free tier, PostgreSQL for production
    database_url: str = "sqlite+aiosqlite:///./golocalchina.db"
    # JWT
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7
    # Platform
    platform_name: str = "GoLocalChina"
    # CORS
    cors_origins: str = "*"  # Set to your Vercel URL in production

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
