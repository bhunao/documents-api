from sqlmodel import Field
from sqlmodel import SQLModel


class Post(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    content: str
