from fastapi import FastAPI
from src.posts.router import router as posts_router
from src.auth.router import router as auth_router

from src.config import settings

app = FastAPI()


app.include_router(posts_router, prefix="/posts", tags=["Posts"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
