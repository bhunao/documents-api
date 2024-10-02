import logging

from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager, contextmanager
from typing import Any

from alembic import command
from alembic.config import Config
from app.core.config import settings
from fastapi import FastAPI, Request
from pydantic.fields import FieldInfo
from sqlmodel import select

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


def stringfy_name(obj: Any):
    """return a string of the object __name__ property"""
    return str(obj.__name__)

def name_n_desc(func: Callable[[Any | None], Any]):
    return f"{func.__name__}: {func.__doc__}"

def is_db_connected():
    return True if database_connection() is True else False


def get_db_connection_msg():
    connected = database_connection()
    if connected is True:
        return str(engine.raw_connection().dialect)
    else:
        return str(connected)

