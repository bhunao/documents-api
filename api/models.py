from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


now = datetime.now()


class DocumentSchema(BaseModel):
    name: str = Field(...)
    path: str = Field(...)
    content: str = Field(...)
    date_added: datetime = Field(...)
    tags: List[str] = Field(...)
    references: List[str] = Field(...)
    last_updated: datetime = Field(...)
    acess: int = Field(...)
    type: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "example name",
                "path": "",
                "content": "content example lorem ipsum something something whatever",
                "date_added": now,
                "tags": ["example"],
                "references": ["example"],
                "last_updated": now,
                "acess": 0,
                "type": "document"
            }
        }


class UpdateDocumentSchema(BaseModel):
    name: Optional[str]
    path: Optional[str]
    content: Optional[str]
    date_added: Optional[datetime]
    tags: Optional[List[str]]
    references: Optional[List[str]]
    last_updated: Optional[datetime]
    acess: Optional[int]
    type: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "example name",
                "path": "",
                "content": "content example lorem ipsum something something whatever",
                "date_added": now,
                "tags": ["example"],
                "references": ["example"],
                "last_updated": now,
                "acess": 0,
                "type": "document"
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(code, message, error="An error occurred"):
    return {"error": error, "code": code, "message": message}
