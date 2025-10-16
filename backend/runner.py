import asyncio

from backend.api.app import ApiApp
from backend.settings import Settings
from backend.tg_bot.app import BotApp


async def run():
    settings = Settings()
    bot_app = BotApp(settings)
    api_app = ApiApp(settings.api)

    await asyncio.gather(bot_app.run(), api_app.run())
