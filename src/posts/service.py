from sqlalchemy.orm import Session
from src.posts import models, schemas
from datetime import datetime
from src.posts.exceptions import PostNotFound


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()


def create_post(db: Session, post: schemas.PostCreate):
    now = datetime.now()
    db_post = models.Post(**post.dict(), created_at=now, updated_at=now)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_post_by_id(db: Session, post_id: int):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise PostNotFound
    return post


def update_post_by_id(db: Session, post_id: int, post: schemas.PostUpdate):
    db_post: models.Post = db.query(models.Post).filter(
        models.Post.id == post_id).first()

    if not db_post:
        raise PostNotFound

    for key, value in post.dict(exclude_unset=True).items():
        setattr(db_post, key, value)

    db_post.updated_at = datetime.now()
    db.commit()
    db.refresh(db_post)

    return db_post


def delete_post_by_id(db: Session, post_id: int):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not db_post:
        raise PostNotFound

    db.delete(db_post)
    db.commit()

    return db_post
