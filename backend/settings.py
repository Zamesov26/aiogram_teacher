from pydantic import Field
from pydantic_settings import BaseSettings

from backend.admin.settings import AdminSettings
from backend.api.settings import APISettings
from backend.database.settings import DBSettings
from backend.tg_bot.config import TGSettings


class Settings(BaseSettings):
    tg: TGSettings = Field(default_factory=TGSettings)
    api: APISettings = Field(default_factory=APISettings)
    db: DBSettings = Field(default_factory=DBSettings)
    admin: AdminSettings = Field(default_factory=AdminSettings)
