from typing import Annotated
from datetime import date

from sqlmodel import Field

from sqlmodel import SQLModel, Field


class BaseTransaction(SQLModel):
    date: date
    type: str
    destiny: str
    value: float

class TransactionCreate(BaseTransaction):
    pass


class Transaction(BaseTransaction, table=True):
    id: int = Field(primary_key=True)

