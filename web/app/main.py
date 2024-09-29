from collections.abc import Callable
import logging
from typing import Any
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.v1.base import router as base_router
from app.core.router import router as core_router
from app.core.main import settings
from app.core.utils import lifespan


logging.basicConfig(level=logging.DEBUG)

app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan
)

app.mount(
    "/static",
    StaticFiles(directory="static/"),
    name="static"
)

app.include_router(base_router)
app.include_router(core_router)
