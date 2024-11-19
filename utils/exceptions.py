from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    ValidationError,
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied,
    NotFound,
    APIException
)
from rest_framework_simplejwt.exceptions import TokenError

from utils.response import CustomResponse


class ConflictException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'A conflict occurred.'
    default_code = 'conflict'


def custom_exception_handler(exc, context):
    """
    Custom exception handler for Django REST framework
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    # If this is a REST framework exception, customize it
    if isinstance(exc, ValidationError):
        return CustomResponse.error(
            message="Validation failed",
            errors=exc.detail,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    elif isinstance(exc, ConflictException):
        return CustomResponse.error(
            message="Conflict error",
            errors=exc.detail,
            status_code=status.HTTP_409_CONFLICT
        )

    elif isinstance(exc, AuthenticationFailed):
        return CustomResponse.error(
            message="Authentication failed",
            errors={"detail": "Invalid credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    elif isinstance(exc, NotAuthenticated):
        return CustomResponse.error(
            message="Authentication required",
            errors={"detail": "Authentication credentials were not provided"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    elif isinstance(exc, PermissionDenied):
        return CustomResponse.error(
            message="Permission denied",
            errors={"detail": "You do not have permission to perform this action"},
            status_code=status.HTTP_403_FORBIDDEN
        )

    elif isinstance(exc, NotFound):
        return CustomResponse.error(
            message="Not found",
            errors={"detail": "Requested resource not found"},
            status_code=status.HTTP_404_NOT_FOUND
        )

    elif isinstance(exc, TokenError):
        return CustomResponse.error(
            message="Token error",
            errors={"detail": "Invalid token"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    # For any other exceptions, return a generic server error
    return CustomResponse.error(
        message="Server error",
        errors={"detail": "An unexpected error occurred"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
