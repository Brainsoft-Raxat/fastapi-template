from fastapi import FastAPI
from src.posts.router import router as posts_router

app = FastAPI()


app.include_router(posts_router, prefix="/posts", tags=["Posts"])