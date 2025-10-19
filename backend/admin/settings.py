from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AdminSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="ADMIN_", extra="ignore"
    )

    name: str = Field("admin")
    password: str = Field("admin")
    telegram_id: int | None = Field(None)
