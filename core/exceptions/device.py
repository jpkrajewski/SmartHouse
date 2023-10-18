from core.exceptions import CustomException
from http import HTTPStatus


class DeviceNotFoundException(CustomException):
    code = HTTPStatus.NOT_FOUND
    error_code = "DEVICE__NOT_FOUND"
    message = "device not found"
