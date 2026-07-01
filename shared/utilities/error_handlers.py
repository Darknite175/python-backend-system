from datetime import datetime
from typing import Dict, Any, Optional


class ErrorResponse:
    """Standard error response format"""

    def __init__(
        self,
        error: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        status_code: int = 400
    ):
        self.error = error
        self.message = message
        self.details = details or {}
        self.status_code = status_code
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "error": self.error,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp
        }


class AppError(Exception):
    """Base application error"""
    def __init__(self, message: str, error_code: str = "ERROR", status_code: int = 400, details: Dict = None):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(AppError):
    """Validation error"""
    def __init__(self, message: str, details: Dict = None):
        super().__init__(message, "VALIDATION_ERROR", 400, details)


class NotFoundError(AppError):
    """Resource not found error"""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, "NOT_FOUND", 404)


class UnauthorizedError(AppError):
    """Unauthorized error"""
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, "UNAUTHORIZED", 401)


class ForbiddenError(AppError):
    """Forbidden error"""
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, "FORBIDDEN", 403)


class ConflictError(AppError):
    """Conflict error (duplicate resource)"""
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, "CONFLICT", 409)


class ServerError(AppError):
    """Internal server error"""
    def __init__(self, message: str = "Internal server error"):
        super().__init__(message, "SERVER_ERROR", 500)
