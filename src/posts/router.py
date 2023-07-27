from typing import Annotated
from fastapi import APIRouter, Depends
from src.posts.schemas import PostCreate, Post, PostUpdate
from src.dependencies import get_db
from typing import List
from src.database import engine
from sqlalchemy.orm import Session

from src.posts import models, service as service

router = APIRouter()

models.Base.metadata.create_all(bind=engine)


@router.get("/", response_model=List[Post])
async def read_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.get_posts(db=db, skip=skip, limit=limit)


@router.post("/", response_model=Post)
async def create(post_data: PostCreate, db: Session = Depends(get_db)):
    return service.create_post(db=db, post=post_data)


@router.get("/{post_id}", response_model=Post)
async def read(post_id: int, db: Session = Depends(get_db)):
    return service.get_post_by_id(db=db, post_id=post_id)


@router.put("/{post_id}", response_model=Post)
async def update(post_id: int, post_data: PostUpdate, db: Session = Depends(get_db)):
    return service.update_post_by_id(db=db, post_id=post_id, post=post_data)


@router.delete("/{post_id}")
async def delete(post_id: int, db: Session = Depends(get_db)):
    return service.delete_post_by_id(db=db, post_id=post_id)
