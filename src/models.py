from datetime import date
from typing import Optional

from sqlmodel import Field

from src.core.database import MODEL


class ExampleModelSchema(MODEL):
    name: str
    favorite_number: int
    date: date


class ExampleModel(MODEL, table=True):
    __tablename__ = "example_model"

    id: Optional[int] = Field(nullable=False, primary_key=True)
    name: str
    favorite_number: int
    date: date
