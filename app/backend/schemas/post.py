from typing import Optional
from sqlmodel import SQLModel


class Post(SQLModel):
    title: str
    content: Optional[str] = None
