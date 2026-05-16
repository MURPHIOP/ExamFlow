from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ExamFlow"
    company_name: str = "M.B. Technosoft Pvt Ltd"
    app_env: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    backend_cors_origins: list[str] | str = ["http://localhost:3000"]
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/examflow"
    direct_database_url: str | None = None

    # JWT Configuration
    jwt_secret_key: str = "change-this-secret-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    password_min_length: int = 8

    # Razorpay Configuration
    razorpay_key_id: str | None = None
    razorpay_key_secret: str | None = None
    razorpay_webhook_secret: str | None = None

    # Frontend URLs
    next_public_app_url: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

    @field_validator("backend_cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return ["http://localhost:3000"]


@lru_cache
def get_settings() -> Settings:
    return Settings()
