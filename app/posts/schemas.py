from typing import Optional
from app.users.models import User

from sqlmodel import Field, Relationship, SQLModel


class PostCreate(SQLModel):
    title: str = Field(index=True)
    content: str = Field(index=True)


class Post(SQLModel):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    content: str = Field(index=True)
    owner_id: int = Field(default=None, foreign_key="user.id")
    owner: Optional[User] = Relationship(back_populates="Users")
