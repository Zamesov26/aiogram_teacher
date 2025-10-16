from fastapi import FastAPI
from .handlers.router import api_router


class ApiApp:
    """Приложение FastAPI."""

    def __init__(self, settings):
        self.settings = settings
        self.app = FastAPI(title=self.settings.title, version=self.settings.version)
        self.app.include_router(api_router)

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
