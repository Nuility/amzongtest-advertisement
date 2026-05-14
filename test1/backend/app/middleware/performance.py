from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import get_settings
from app.core.logger import logger
import time


class PerformanceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        settings = get_settings()
        start_time = time.time()
        
        response = await call_next(request)
        
        duration = time.time() - start_time
        
        if duration > settings.performance_slow_request_threshold:
            logger.warning(
                f"Slow request detected",
                extra={
                    'method': request.method,
                    'path': request.url.path,
                    'duration_seconds': round(duration, 3),
                    'threshold': settings.performance_slow_request_threshold
                }
            )
        
        response.headers['X-Response-Time'] = f"{round(duration * 1000, 2)}ms"
        
        return response
