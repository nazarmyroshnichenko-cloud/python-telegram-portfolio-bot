from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str = Field(..., alias="BOT_TOKEN")
    admin_id: int = Field(..., alias="ADMIN_ID")
    database_url: str = Field(..., alias="DATABASE_URL")
    default_language: str = Field("en", alias="DEFAULT_LANGUAGE")
    github_url: str = Field("https://github.com/nazarmyroshnichenko-cloud", alias="GITHUB_URL")
    telegram_username: str = Field("i_amnazi66", alias="TELEGRAM_USERNAME")
    contact_email: str = Field("nazarmyroshnichenko@gmail.com", alias="CONTACT_EMAIL")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", populate_by_name=True)

    @field_validator("database_url")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        if value.startswith("postgres://"):
            return value.replace("postgres://", "postgresql+asyncpg://", 1)
        if value.startswith("postgresql://"):
            return value.replace("postgresql://", "postgresql+asyncpg://", 1)
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
