from fastapi import APIRouter, status, Depends, Response, BackgroundTasks
from src.auth.schemas import AuthUser, UserResponse, AccessTokenResponse, JWTData
from src.dependencies import get_db
from src.auth.dependencies import valid_user_create, valid_refresh_token, valid_refresh_token_user
from src.auth.jwt import parse_jwt_user_data
from src.auth import service
from sqlalchemy.orm import Session
from src.database import engine
from src.auth import models, utils, jwt


router = APIRouter()

models.Base.metadata.create_all(bind=engine)


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(auth_data: AuthUser = Depends(valid_user_create), db: Session = Depends(get_db)):
    user = service.create_user(db, auth_data)
    return {
        "id": user.id,
        "email": user.email
    }


@router.get("/users/me", response_model=UserResponse)
async def get_my_account(
        jwt_data: JWTData = Depends(parse_jwt_user_data), db: Session = Depends(get_db)
) -> dict[str, str]:
    user = service.get_user_by_id(db, jwt_data.id)

    return {
        "id": user.id,
        "email": user.email
    }


@router.post("/users/tokens", response_model=AccessTokenResponse)
async def auth_user(auth_data: AuthUser, response: Response, db: Session = Depends(get_db)) -> AccessTokenResponse:
    user = service.authenticate_user(db, auth_data)
    refresh_token_value = service.create_refresh_token(db=db, user_id=user.id)

    response.set_cookie(
        **utils.get_refresh_token_settings(refresh_token_value))

    return AccessTokenResponse(
        access_token=jwt.create_access_token(user=user),
        refresh_token=refresh_token_value
    )

@router.put("/users/tokens", response_model=AccessTokenResponse)
async def refresh_tokens(
    worker: BackgroundTasks,
    response: Response,
    refresh_token: models.RefreshToken = Depends(valid_refresh_token),
    user: models.User = Depends(valid_refresh_token_user),
    db: Session = Depends(get_db)
) -> AccessTokenResponse:
    refresh_token_value = service.create_refresh_token(
        db = db,
        user_id=refresh_token.user_id
    )
    response.set_cookie(**utils.get_refresh_token_settings(refresh_token_value))

    worker.add_task(service.expire_refresh_token, db, refresh_token.uuid)
    return AccessTokenResponse(
        access_token=jwt.create_access_token(user=user),
        refresh_token=refresh_token_value,
    )

@router.delete("/users/tokens")
async def logout_user(
    response: Response,
    refresh_token: models.RefreshToken = Depends(valid_refresh_token),
    db: Session = Depends(get_db)
) -> None:
    service.expire_refresh_token(db, refresh_token.uuid)

    response.delete_cookie(
        **utils.get_refresh_token_settings(refresh_token.refresh_token, expired=True)
    )