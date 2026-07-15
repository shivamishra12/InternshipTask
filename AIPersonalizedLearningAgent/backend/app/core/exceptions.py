class AppException(Exception):
    """Base exception class for all application-specific errors"""
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class ModelLoadError(AppException):
    """Raised when an ML model fails to load successfully"""
    def __init__(self, message: str):
        super().__init__(message, status_code=500)


class PredictionError(AppException):
    """Raised when an ML model prediction/inference fails"""
    def __init__(self, message: str):
        super().__init__(message, status_code=500)


class StudentNotFoundError(AppException):
    """Raised when the requested student cannot be found"""
    def __init__(self, student_id: int):
        super().__init__(f"Student with ID {student_id} was not found in the records.", status_code=404)


class InvalidRequestError(AppException):
    """Raised when request data is invalid or inconsistent"""
    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class ValidationFailedError(AppException):
    """Raised when a strict verification validation fails"""
    def __init__(self, message: str):
        super().__init__(message, status_code=422)
