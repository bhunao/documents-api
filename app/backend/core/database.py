import logging
from sqlmodel import SQLModel
from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import Secret

from sqlmodel import create_engine
from sqlmodel import Session

config = Config(".env")
logging.basicConfig(format="[%(asctime)s | %(levelname)s | %(name)s.%(funcName)s]: %(message)s")

PROJECT_NAME = "phresh"
VERSION = "1.0.0"
API_PREFIX = "/api"

SECRET_KEY = config("SECRET_KEY", cast=Secret, default="CHANGEME")

POSTGRES_USER = config("POSTGRES_USER", cast=str)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str, default="db")
POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default="5432")
POSTGRES_DB = config("POSTGRES_DB", cast=str)

DATABASE_URL = config(
    "DATABASE_URL",
    cast=DatabaseURL,
    default=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
postgre_url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(postgre_url, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    with Session(engine) as session:
        yield session
