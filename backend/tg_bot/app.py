import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Update
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from backend.settings import Settings
from backend.tg_bot.config import TGSettings
from backend.tg_bot.midlewars.setup import setup_middlewares
from backend.tg_bot.queue.protocol import AsyncQueueProtocol
from .collector.polling import PollingCollector
from .handlers import setup_routers
from .processor.aiogram_proc import AiogramProcessor


class BotApp:
    """Приложение Telegram-бота."""

    def __init__(
        self, settings: Settings, queue: AsyncQueueProtocol[Update] | None = None
    ):
        self.bot = Bot(token=settings.tg.token)
        self.dp = Dispatcher()
        self.dp.include_router(setup_routers())
        
        engine = create_async_engine(settings.db.url)
        session_factory = async_sessionmaker(engine, expire_on_commit=False)
        
        setup_middlewares(self.dp, session_factory=session_factory)

        if not queue:
            self.queue = asyncio.Queue()

        self.collector = PollingCollector(self.bot, self.queue)
        self.processor = AiogramProcessor(self.bot, self.dp, self.queue)

    async def run(self):
        """Запуск Collector + Processor."""
        await asyncio.gather(self.collector.run(), self.processor.run())


if __name__ == "__main__":
    tg_settings = TGSettings()
    app = BotApp(settings=tg_settings)
    asyncio.run(app.run())
