from http import HTTPStatus


class CustomException(Exception):
    """Base class for all exceptions. Override those fields."""

    def __init__(self, message=None):
        if message:
            self.message = message


class UnauthorizedException(CustomException):
    code = HTTPStatus.UNAUTHORIZED
    error_code = HTTPStatus.UNAUTHORIZED
    message = HTTPStatus.UNAUTHORIZED.description
