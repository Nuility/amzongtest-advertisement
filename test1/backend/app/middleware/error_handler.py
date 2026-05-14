from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.core.exceptions import BaseAPIException
from app.core.context import get_request_id
from app.core.logger import logger
from datetime import datetime


async def global_exception_handler(request: Request, exc: Exception):
    request_id = get_request_id() or "unknown"
    
    if isinstance(exc, BaseAPIException):
        logger.error(
            f"API Exception: {exc.error_code} - {exc.message}",
            extra={
                'request_id': request_id,
                'error_code': exc.error_code,
                'status_code': exc.status_code,
                'details': exc.details
            }
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                'error_code': exc.error_code,
                'message': exc.message,
                'details': exc.details,
                'request_id': request_id,
                'timestamp': datetime.utcnow().isoformat()
            }
        )
    
    elif isinstance(exc, RequestValidationError):
        errors = exc.errors()
        logger.warning(
            f"Validation error: {errors}",
            extra={
                'request_id': request_id,
                'errors': errors
            }
        )
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                'error_code': 'VALIDATION_ERROR',
                'message': 'Request validation failed',
                'details': errors,
                'request_id': request_id,
                'timestamp': datetime.utcnow().isoformat()
            }
        )
    
    elif isinstance(exc, SQLAlchemyError):
        logger.error(
            f"Database error: {str(exc)}",
            extra={
                'request_id': request_id
            },
            exc_info=True
        )
        
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                'error_code': 'DATABASE_ERROR',
                'message': 'Database operation failed',
                'request_id': request_id,
                'timestamp': datetime.utcnow().isoformat()
            }
        )
    
    else:
        logger.error(
            f"Unexpected error: {str(exc)}",
            extra={
                'request_id': request_id
            },
            exc_info=True
        )
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                'error_code': 'INTERNAL_ERROR',
                'message': 'An unexpected error occurred',
                'request_id': request_id,
                'timestamp': datetime.utcnow().isoformat()
            }
        )
