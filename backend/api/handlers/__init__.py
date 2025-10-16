from fastapi import APIRouter


def register_routes(app):
    """Register all API routes with the FastAPI application"""
    health_handler = HealthHandler()

    app.include_router(health_handler.router, prefix="/api", tags=["health"])
