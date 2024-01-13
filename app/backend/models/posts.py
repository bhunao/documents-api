from typing import Optional
from sqlmodel import Field, SQLModel


class Post(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    content: Optional[str] = None
