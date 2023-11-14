from http import HTTPStatus

from core.exceptions import CustomException


class DeviceNotFoundException(CustomException):
    code = HTTPStatus.NOT_FOUND
    error_code = "DEVICE__NOT_FOUND"
    message = "device not found"
