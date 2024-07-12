from sqlalchemy.exc import OperationalError
import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import Session

from app.core import db as database


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print("============== saerasaybiryirbi")
        # database.create_db_and_tables()
    except OperationalError as ex:
        logger.error(f"database Operational Error error {ex}")

    assert app is not None
    yield
    logger.info("Closing application lifespan.")
