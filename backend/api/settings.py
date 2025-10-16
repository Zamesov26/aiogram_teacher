from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class APISettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="API_", extra="ignore"
    )

    host: str = Field("localhost")
    port: int = Field(8080)
    reload: bool = Field(True)
    title: str = Field("App API")
    version: str = Field("0.1.0")
