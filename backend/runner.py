import asyncio

from backend.api.app import ApiApp
from backend.database.engine import db_session_factory
from backend.settings import Settings
from backend.tg_bot.app import BotApp


async def run():
    settings = Settings()
    
    bot_app = BotApp(settings.tg, db_session_factory=db_session_factory)
    api_app = ApiApp(settings.api)

    await asyncio.gather(bot_app.run(), api_app.run())
