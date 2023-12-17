from sqlmodel import Field
from sqlmodel import SQLModel


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    password: str
    # created_at:
    active_user: bool = True


class UserSchema(SQLModel):
    name: str
    password: str


class News(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    content: str


class NewsSchema(SQLModel):
    title: str
    content: str
