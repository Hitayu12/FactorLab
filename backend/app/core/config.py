from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "postgresql+psycopg://factorlab:factorlab@postgres:5432/factorlab"
    REDIS_URL: str = "redis://redis:6379/0"
    ENV: str = "dev"
    CORS_ALLOW_ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]


settings = Settings()
