import abc

from backend.tg_bot.queue.protocol import AsyncQueueProtocol


class AbstractProcessor(abc.ABC):
    """Базовый интерфейс для обработки апдейтов из очереди."""

    def __init__(self, queue: AsyncQueueProtocol):
        self.queue = queue

    @abc.abstractmethod
    async def run(self) -> None:
        """Главный цикл обработки."""
        ...
