"""Application configuration — env-driven via pydantic-settings."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql+asyncpg://glc:glc_secret@localhost:5432/golocalchina"
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    # JWT
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7
    # Platform
    platform_fee_pct: float = 12.00  # 信息服务费 (Information Service Fee)
    platform_name: str = "GoLocalChina"
    # Airwallex
    airwallex_api_key: str = ""
    airwallex_webhook_secret: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
