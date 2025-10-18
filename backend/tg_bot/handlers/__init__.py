from aiogram import Router
from . import initial, start, main_menu


def setup_routers() -> Router:
    router = Router()
    router.include_router(start.router)
    router.include_router(main_menu.router)
    router.include_router(initial.router)
    return router
