import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response


class RequestValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Add any request validation logic here
        response = await call_next(request)
        return response


def add_middlewares(app):
    """Add all middleware to the FastAPI application"""
    app.add_middleware(TimingMiddleware)
    # Add other middleware as needed
    # app.add_middleware(RequestValidationMiddleware)
