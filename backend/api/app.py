from fastapi import FastAPI
from sqladmin import Admin

from .handlers.router import api_router
from ..admin.app import DatabaseAuth, LessonAdmin, TaskAdmin, TeacherAdmin
from ..database.engine import engine


class ApiApp:
    """Приложение FastAPI."""

    def __init__(self, settings):
        self.settings = settings
        self.app = FastAPI(title=self.settings.title, version=self.settings.version)
        self.app.include_router(api_router)
        admin = Admin(self.app, engine, authentication_backend=DatabaseAuth(secret_key="super-secret"))

        admin.add_view(LessonAdmin)
        admin.add_view(TaskAdmin)
        admin.add_view(TeacherAdmin)
        
    async def run(self):
        """Запуск FastAPI через Uvicorn."""
        import uvicorn

        config = uvicorn.Config(
            self.app,
            host=self.settings.host,
            port=self.settings.port,
            reload=self.settings.reload,
            log_level="info",
        )
        server = uvicorn.Server(config)
        await server.serve()
