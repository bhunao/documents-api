import logging

from typing import Generator
from sqlalchemy.exc import OperationalError

from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import Session

from src.core.database import MODEL, engine


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        MODEL.metadata.create_all(engine)
    except OperationalError as ex:
        logger.error(f"database Operational Error error {ex}")

    assert app is not None
    yield
    logger.info("Closing application lifespan.")


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
