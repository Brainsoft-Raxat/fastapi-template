from sqlalchemy import Column, Integer, String, Text, DateTime
from src.database import Base


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    author = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
