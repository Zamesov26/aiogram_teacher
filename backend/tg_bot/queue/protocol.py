from typing import Protocol, TypeVar, runtime_checkable

T = TypeVar("T")


@runtime_checkable
class AsyncQueueProtocol(Protocol[T]):
    async def put(self, item: T) -> None:
        """Извлечь элемент из очереди."""

    async def get(self) -> T:
        """Добавить элемент в очередь."""
