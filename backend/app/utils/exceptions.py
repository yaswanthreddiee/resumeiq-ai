"""Custom exceptions."""


class AppException(Exception):
    """Base application exception."""
    
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundException(AppException):
    """Resource not found."""
    
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, 404)


class BadRequestException(AppException):
    """Invalid request."""
    
    def __init__(self, message: str = "Bad request"):
        super().__init__(message, 400)


class ConflictException(AppException):
    """Resource conflict."""
    
    def __init__(self, message: str = "Conflict"):
        super().__init__(message, 409)


class UnauthorizedException(AppException):
    """Unauthorized access."""
    
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, 401)


class ForbiddenException(AppException):
    """Forbidden access."""
    
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, 403)


class InternalServerException(AppException):
    """Internal server error."""
    
    def __init__(self, message: str = "Internal server error"):
        super().__init__(message, 500)
