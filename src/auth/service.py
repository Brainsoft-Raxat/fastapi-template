import uuid
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from src.auth import schemas, models
from src.auth.security import hash_password, check_password
from src.auth.exceptions import InvalidCredentials, UserNotFound
from src.utils import generate_random_alphanum
from src.auth.config import auth_config


def create_user(db: Session, user: schemas.AuthUser):
    db_user = models.User()
    db_user.email = user.email
    db_user.hashed_password = hash_password(user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    return user


def get_user_by_id(db: Session, user_id: str):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise UserNotFound
    return user


def authenticate_user(db: Session, auth_data: schemas.AuthUser):
    user = get_user_by_email(db, auth_data.email)
    if not user:
        raise InvalidCredentials()
    if not check_password(auth_data.password, user.hashed_password):
        raise InvalidCredentials()

    return user


def create_refresh_token(
        *, db: Session, user_id: int, refresh_token: str | None = None
) -> str:
    if not refresh_token:
        refresh_token = generate_random_alphanum(64)

    db_refresh_token = models.RefreshToken(
        uuid=str(uuid.uuid4()),
        user_id=user_id,
        refresh_token=refresh_token,
        expires_at=datetime.utcnow() + timedelta(seconds=auth_config.REFRESH_TOKEN_EXP),
    )
    db.add(db_refresh_token)
    db.commit()
    db.refresh(db_refresh_token)

    return refresh_token


def get_refresh_token(db: Session, refresh_token: str) -> models.RefreshToken | None:
    db_refresh_token = db.query(models.RefreshToken).filter(
        models.RefreshToken.refresh_token == refresh_token).first()
    return db_refresh_token


def expire_refresh_token(db: Session, refresh_token_uuid: uuid.UUID) -> None:
    db_refresh_token: models.RefreshToken = db.query(models.RefreshToken).filter(
        models.RefreshToken.uuid == refresh_token_uuid).first()
    db_refresh_token.expires_at = datetime.utcnow() - timedelta(days=1)
    db.commit()
    db.refresh(db_refresh_token)
