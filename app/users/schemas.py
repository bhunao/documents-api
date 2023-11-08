from typing import List
from app.posts.models import Post

from sqlmodel import Field, Relationship, SQLModel


class UserCreate(SQLModel):
    username: str = Field(unique=True, index=True)
    password: str
    posts: List["Post"] = Relationship(back_populates="Post")


class User(SQLModel):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    is_active: bool = True
    posts: List["Post"] = Relationship(back_populates="Post")
