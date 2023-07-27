import re
from pydantic import BaseModel, EmailStr, Field, validator

STRONG_PASSWORD_PATTERN = re.compile(
    r"^(?=.*[\d])(?=.*[!@#$%^&*])[\w!@#$%^&*]{6,128}$")


class AuthUser(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

    @validator("password")
    def valid_password(cls, password: str) -> str:
        if not re.match(STRONG_PASSWORD_PATTERN, password):
            raise ValueError(
                "Password must contain at least "
                "one lower character, "
                "one upper character, "
                "digit or "
                "special symbol"
            )

        return password

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    email: EmailStr


class AccessTokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class JWTData(BaseModel):
    id: int = Field(alias="sub")
