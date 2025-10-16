from pydantic_settings import BaseSettings, SettingsConfigDict


class TGSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="TG_",
        extra="ignore",
    )

    token: str
    log_dir: str = "logs/"
