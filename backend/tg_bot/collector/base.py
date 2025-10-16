import abc

from backend.tg_bot.queue.protocol import AsyncQueueProtocol


class AbstractCollector(abc.ABC):
    """Базовый интерфейс для получения апдейтов."""

    def __init__(self, queue: AsyncQueueProtocol):
        self.queue = queue

    @abc.abstractmethod
    async def run(self) -> None:
        """Главный цикл получения апдейтов и помещения их в очередь."""
        ...
