import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import Session

from . import database


logger = logging.getLogger(__name__)


def get_session() -> Session:
    with Session(database.engine) as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.create_db_and_tables()
    logger.info("starting lifespan...")
    assert app is not None
    yield
    logger.info("...ending lifespan")
