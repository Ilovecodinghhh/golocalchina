"""Environment-driven config via Pydantic Settings.

PIPL note: any default that touches PII must remain China-region.
"""
from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ---- runtime ----
    env: Literal["dev", "staging", "prod"] = "dev"
    debug: bool = False
    app_name: str = "ctrip-guides-api"
    api_v1_prefix: str = "/api/v1"

    # ---- database ----
    # async URL is what the app uses; sync URL is what Alembic uses.
    postgres_user: str = "ctrip"
    postgres_password: str = "ctrip"
    postgres_db: str = "ctrip_guides"
    postgres_host: str = "db"
    postgres_port: int = 5432

    @property
    def database_url_async(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def database_url_sync(self) -> str:
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    # ---- redis ----
    redis_url: RedisDsn = Field(default="redis://redis:6379/0")

    # ---- auth ----
    jwt_secret: str = "CHANGE_ME_IN_PROD_USE_RS256"
    jwt_algorithm: str = "HS256"
    jwt_access_minutes: int = 15
    jwt_refresh_days: int = 14

    # ---- payments ----
    airwallex_api_base: str = "https://api.airwallex.com"
    airwallex_client_id: str = ""
    airwallex_api_key: str = ""

    # ---- compliance / PIPL ----
    data_region: Literal["cn-hangzhou", "cn-beijing", "ap-singapore"] = "cn-hangzhou"
    enable_cross_border_consent: bool = True

    # ---- CORS ----
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:19006",  # Expo
    ]

    # ---- i18n ----
    supported_locales: list[str] = ["en-US", "zh-CN", "ja-JP", "ko-KR", "fr-FR"]
    default_locale: str = "en-US"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
