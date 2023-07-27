from fastapi import Depends, Cookie
from src.dependencies import get_db
from src.auth.exceptions import EmailTaken, RefreshTokenNotValid
from src.auth import service, models
from src.auth.schemas import AuthUser
from sqlalchemy.orm import Session
from datetime import datetime
import time


def valid_user_create(user: AuthUser, db: Session = Depends(get_db)) -> AuthUser:
    db_user = service.get_user_by_email(db, user.email)
    if db_user:
        raise EmailTaken
    return user


def valid_refresh_token(
    db: Session = Depends(get_db),
    refresh_token: str = Cookie(..., alias="refreshToken"),
) -> models.RefreshToken:
    db_refresh_token = service.get_refresh_token(db, refresh_token)
    if not db_refresh_token:
        raise RefreshTokenNotValid()

    if not _is_valid_refresh_token(db_refresh_token):
        raise RefreshTokenNotValid()

    return db_refresh_token


def valid_refresh_token_user(
    db: Session = Depends(get_db),
    refresh_token: models.RefreshToken = Depends(valid_refresh_token),
) -> models.User:
    user = service.get_user_by_id(db, refresh_token.user_id)
    if not user:
        raise RefreshTokenNotValid()

    return user


def _is_valid_refresh_token(db_refresh_token: models.RefreshToken) -> bool:
    return datetime.utcnow() <= db_refresh_token.expires_at
