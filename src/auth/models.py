from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from src.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(LargeBinary, nullable=False)


class RefreshToken(Base):
    __tablename__ = "auth_refresh_tokens"
    uuid = Column(UUID, primary_key=True)
    user_id = Column(ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    refresh_token = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now())
