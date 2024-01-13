from typing import Optional
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: Optional[int] = Field(nullable=False, primary_key=True)
    username: str = Field(unique=True)
    password: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: bool = False
