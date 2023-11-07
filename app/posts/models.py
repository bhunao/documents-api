from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from ..users.models import User


class Post(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    content: str = Field(index=True)

    owner_id: int = Field(default=None, foreign_key="user.id")
    owner: Optional[User] = Relationship(back_populates="posts")
