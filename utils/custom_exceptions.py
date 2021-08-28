from utils.constants import RESPONSE_ERROR_FORBIDDEN


class CustomGeneralException(Exception):
    _status_code = None
    _message = ''

    @property
    def status_code(self):
        return self._status_code

    @property
    def message(self):
        return self._message

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self._status_code = 500


class ServerException(CustomGeneralException):
    def __init__(self, *args: object, message=None, **kwargs) -> None:
        super().__init__(*args)
        self._status_code = 500
        self._message = message


class BadRequestException(CustomGeneralException):
    def __init__(self, *args: object, message=None, **kwargs) -> None:
        super().__init__(*args)
        self._status_code = 400
        self._message = message


class ForbiddenException(CustomGeneralException):
    def __init__(self, *args: object, message=None, **kwargs) -> None:
        super().__init__(*args)
        self._status_code = 403
        self._message = RESPONSE_ERROR_FORBIDDEN if message is None else message
