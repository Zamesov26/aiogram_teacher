from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    """Простой ответ на команду /start."""
    await message.answer(
        "👋 Привет! Я бот с архитектурой на очереди.\n"
        "Я получаю обновления через Polling и обрабатываю их асинхронно."
    )
