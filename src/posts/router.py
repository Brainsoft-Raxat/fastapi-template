from typing import Annotated
from fastapi import APIRouter, Body
from src.posts.database import db
from src.posts.schemas import PostCreate, Post, PostUpdate
from src.posts.exceptions import PostNotFound
from datetime import datetime
from typing import List

router = APIRouter()


@router.get("/", response_model=List[Post])
async def read_all():
    return db.posts


@router.post("/", response_model=Post)
async def create(post_data: PostCreate):
    current_time = datetime.now()

    db.last_id += 1
    new_post_data = post_data.model_dump()
    new_post_data.update({
        "id": db.last_id,
        "created_at": current_time,
        "updated_at": current_time
    })

    db.posts.append(Post(**new_post_data))

    return db.posts[db.last_id]


@router.get("/{post_id}", response_model=Post)
async def read(post_id: int) -> dict[str, str]:
    for post in db.posts:
        if post.id == post_id:
            return post

    raise PostNotFound


@router.put("/{post_id}", response_model=Post)
async def update(post_id: int, post_data: PostUpdate):
    id = -1
    for i, post in enumerate(db.posts):
        if post.id == post_id:
            id = i

    if id == -1:
        raise PostNotFound

    update_data = post_data.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.today()
    db.posts[id] = db.posts[id].model_copy(update=update_data, deep=True)

    return db.posts[id]


@router.delete("/{post_id}")
async def delete(post_id: int):
    id = -1
    for i, post in enumerate(db.posts):
        if post.id == post_id:
            id = i

    if id == -1:
        raise PostNotFound

    del db.posts[id]
    return
