from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = True

    posts: List["Post"] = Relationship(back_populates="owner")


class Post(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    content: str = Field(index=True)

    owner_id: int = Field(default=None, foreign_key="user.id")
    owner: Optional[User] = Relationship(back_populates="posts")
