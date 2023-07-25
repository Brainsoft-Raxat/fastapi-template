from src.posts.schemas import Post
from datetime import datetime
from typing import List


class DB:
    def __init__(self, posts: List[Post], last_id: int):
        self.posts = posts
        self.last_id = last_id

    posts: List[Post]
    last_id: int


db = DB(
    posts=[
        Post(id=0, title="What's up?!", content="Blah Blah", author="Rakhat",
             created_at=datetime.now(), updated_at=datetime.now()),
        Post(id=1, title="Fast API is cool?!", content="Blah Blah",
             author="Yerasyl", created_at=datetime.now(), updated_at=datetime.now()),
        Post(id=2, title="Is backend hard?", content="Blah Blah",
             author="Vitaliy", created_at=datetime.now(), updated_at=datetime.now())
    ],
    last_id=2)
