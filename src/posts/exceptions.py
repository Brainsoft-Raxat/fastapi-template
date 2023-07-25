from src.exceptions import NotFound
from src.posts.constants import ErrorCode

class PostNotFound(NotFound):
    DETAIL = ErrorCode.POST_NOT_FOUND