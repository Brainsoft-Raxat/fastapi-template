from src.auth.constants import ErrorCode
from src.exceptions import BadRequest, NotFound, NotAuthenticated


class EmailTaken(BadRequest):
    DETAIL = ErrorCode.EMAIL_TAKEN

class UserNotFound(NotFound):
    DETAIL = ErrorCode.USER_NOT_FOUND

class InvalidCredentials(NotAuthenticated):
    DETAIL = ErrorCode.INVALID_CREDENTIALS

class InvalidToken(NotAuthenticated):
    DETAIL = ErrorCode.INVALID_TOKEN

class AuthRequired(NotAuthenticated):
    DETAIL = ErrorCode.AUTHENTICATION_REQUIRED

class RefreshTokenNotValid(NotAuthenticated):
    DETAIL = ErrorCode.REFRESH_TOKEN_NOT_VALID