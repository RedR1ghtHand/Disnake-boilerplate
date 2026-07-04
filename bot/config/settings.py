"""Environment variables and secrets loaded via pydantic-settings."""

from functools import lru_cache
from typing import Annotated

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    bot_token: str
    allowed_guilds: Annotated[list[int], NoDecode] = Field(default_factory=list)
    environment: str = "development"
    log_level: str = "INFO"

    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_database: str = "bot"

    members_intent: bool = False
    presences_intent: bool = False
    message_content_intent: bool = True

    @field_validator("allowed_guilds", mode="before")
    @classmethod
    def parse_allowed_guilds(cls, value: object) -> list[int]:
        if value is None or value == "":
            return []
        if isinstance(value, str):
            return [int(item.strip()) for item in value.split(",") if item.strip()]
        if isinstance(value, int):
            return [value]
        return list(value)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
