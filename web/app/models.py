from datetime import datetime
from uuid import uuid4

from pydantic import UUID4
from sqlmodel import SQLModel, Field


class Connection(SQLModel):
    id: UUID4 = Field(primary_key=True, default_factory=uuid4)
    time: datetime = Field(default_factory=datetime.now)
