from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class PostCreate(BaseModel):
    title: str
    content: str
    author: str


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class Post(BaseModel):
    id: int
    title: str
    content: str
    author: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
