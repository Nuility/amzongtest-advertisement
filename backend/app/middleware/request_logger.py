from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.context import set_request_id, get_request_id, clear_context
from app.core.logger import logger
import time


class RequestLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get('X-Request-ID')
        request_id = set_request_id(request_id)
        
        start_time = time.time()
        
        logger.info(
            f"Request started",
            extra={
                'request_id': request_id,
                'method': request.method,
                'path': request.url.path,
                'query_params': str(request.query_params),
                'client_ip': request.client.host if request.client else None
            }
        )
        
        try:
            response = await call_next(request)
            
            duration = time.time() - start_time
            
            logger.info(
                f"Request completed",
                extra={
                    'request_id': request_id,
                    'method': request.method,
                    'path': request.url.path,
                    'status_code': response.status_code,
                    'duration_ms': round(duration * 1000, 2)
                }
            )
            
            response.headers['X-Request-ID'] = request_id
            return response
        
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                f"Request failed: {str(e)}",
                extra={
                    'request_id': request_id,
                    'method': request.method,
                    'path': request.url.path,
                    'duration_ms': round(duration * 1000, 2),
                    'error': str(e)
                },
                exc_info=True
            )
            raise
        finally:
            clear_context()
