import asyncio
from aiogram import Bot
from .base import AbstractCollector
from ..queue.protocol import AsyncQueueProtocol


class PollingCollector(AbstractCollector):
    """Коллектор, который получает апдейты через polling."""

    def __init__(self, bot: Bot, queue: AsyncQueueProtocol, poll_interval: float = 1.0):
        super().__init__(queue)
        self.bot = bot
        self.poll_interval = poll_interval

    async def run(self) -> None:
        offset = 0
        while True:
            updates = await self.bot.get_updates(offset=offset, timeout=30)
            for update in updates:
                await self.queue.put(update)
                offset = max(offset, update.update_id + 1)
            await asyncio.sleep(self.poll_interval)
