from aiogram import Router
from . import start, main_menu, teacher, student


def setup_routers() -> Router:
    router = Router()
    router.include_router(start.router)
    router.include_router(main_menu.router)
    router.include_router(teacher.router)
    router.include_router(student.router)
    return router
