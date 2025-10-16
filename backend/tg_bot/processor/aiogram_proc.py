from aiogram import Dispatcher, Bot
from aiogram.types import Update
from .base import AbstractProcessor
from ..queue.protocol import AsyncQueueProtocol


class AiogramProcessor(AbstractProcessor):
    """Processor, который передаёт апдейты в aiogram Dispatcher."""

    def __init__(self, bot: Bot, dp: Dispatcher, queue: AsyncQueueProtocol):
        super().__init__(queue)
        self.bot = bot
        self.dp = dp

    async def run(self) -> None:
        while True:
            update: Update = await self.queue.get()
            try:
                await self.dp.feed_update(self.bot, update)
            except Exception as e:
                print(f"[Processor] Error handling update: {e}")
