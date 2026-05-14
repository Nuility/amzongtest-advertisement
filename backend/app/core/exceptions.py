from fastapi import HTTPException
from typing import Optional, List, Any


class BaseAPIException(HTTPException):
    def __init__(
        self,
        status_code: int,
        error_code: str,
        message: str,
        details: Optional[List[Any]] = None
    ):
        self.error_code = error_code
        self.message = message
        self.details = details
        super().__init__(status_code=status_code, detail=message)


class DatabaseError(BaseAPIException):
    def __init__(self, message: str = "Database operation failed", details: Optional[List[Any]] = None):
        super().__init__(
            status_code=503,
            error_code="DATABASE_ERROR",
            message=message,
            details=details
        )


class ValidationError(BaseAPIException):
    def __init__(self, message: str = "Validation failed", details: Optional[List[Any]] = None):
        super().__init__(
            status_code=422,
            error_code="VALIDATION_ERROR",
            message=message,
            details=details
        )


class NotFoundError(BaseAPIException):
    def __init__(self, message: str = "Resource not found", details: Optional[List[Any]] = None):
        super().__init__(
            status_code=404,
            error_code="NOT_FOUND",
            message=message,
            details=details
        )


class ExternalAPIError(BaseAPIException):
    def __init__(self, message: str = "External API call failed", details: Optional[List[Any]] = None):
        super().__init__(
            status_code=502,
            error_code="EXTERNAL_API_ERROR",
            message=message,
            details=details
        )


class BusinessError(BaseAPIException):
    def __init__(self, message: str, error_code: str = "BUSINESS_ERROR", status_code: int = 400, details: Optional[List[Any]] = None):
        super().__init__(
            status_code=status_code,
            error_code=error_code,
            message=message,
            details=details
        )


class BidOutOfRangeError(BusinessError):
    def __init__(self, message: str = "Bid amount is out of allowed range", details: Optional[List[Any]] = None):
        super().__init__(
            message=message,
            error_code="BID_OUT_OF_RANGE",
            details=details
        )


class CacheError(BaseAPIException):
    def __init__(self, message: str = "Cache operation failed", details: Optional[List[Any]] = None):
        super().__init__(
            status_code=503,
            error_code="CACHE_ERROR",
            message=message,
            details=details
        )
