from collections.abc import AsyncIterator
from contextlib import asynccontextmanager, contextmanager
import logging
from typing import Any

from alembic import command
from alembic.config import Config
from fastapi import FastAPI, Request
from sqlmodel import select
from pydantic.fields import FieldInfo
from app.core.database import SQLModel
from app.core.config import settings

from app.core.database import get_session

log = logging.getLogger(__name__)


def is_hx_request(request: Request):
    return request.headers.get("Hx-Request") == "true"


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

def database_connection() -> bool | Exception:
    try:
        with contextmanager(get_session)() as session:
            query = select(1)
            _ = session.exec(query).all()
    except Exception as e:
        return e
    return True


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[dict[Any, Any]]:
    log.debug(f"Starting lifespan event of {settings.APP_NAME}.")
    if database_connection() is False:
        log.error("Error trying to connect with the database.")
        # raise Exception("Database not connected.")
    assert app
    state = dict()
    yield state
    log.debug(f"Finishing lifespan event of {settings.APP_NAME}.")

def get_input_type(field: FieldInfo) -> str:
    annotation = field.annotation
    if annotation is int:
        return "number"
    elif annotation is float:
        return "number"
    elif annotation is str:
        return "text"
    elif annotation is bool:
        return "checkbox"
    return "text"

def test_jinja_filter(asd: int) -> str:
    return str(asd)+"mensagem"
