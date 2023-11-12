from contextlib import asynccontextmanager
from fastapi import FastAPI
from icecream import ic
from sqlmodel import SQLModel

from src.database import engine
from src.repository_manager import app_list


@asynccontextmanager
async def lifespan(app: FastAPI):
    assert app is not None
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)
for _app in app_list:
    ic(_app.__name__)
    router = _app.routes.router
    app.include_router(router)
