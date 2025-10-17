from aiogram import Router
from . import initial


def setup_routers() -> Router:
    router = Router()
    router.include_router(initial.router)
    return router
