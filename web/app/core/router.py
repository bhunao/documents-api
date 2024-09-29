from typing import Any, Callable
from sqlmodel import SQLModel
from app.core.main import templates, template_filters
from app.core.config import Settings, settings
from fastapi import APIRouter, Request

from app.core.database import engine
from app.core.utils import database_connection


router = APIRouter(
    prefix="/core",
    tags=["core"],
    dependencies=None # TODO: add user previlege to acess thiss
)

def name_n_desc(func: Callable[[Any], Any]):
    return f"{func.__name__}: {func.__doc__}"


db_connection = database_connection()
if db_connection is True:
    connected = True
    connection = engine.raw_connection().dialect
else:
    connected = False
    assert isinstance(db_connection, Exception)
    connection = str(db_connection)


class DatabaseCheck(SQLModel):
    connected: bool = connected
    connection: str = connection


CONTEXT_PROCESSORS = list(map(name_n_desc, templates.context_processors))
FILTERS = list(map(lambda f: str(f.__name__), template_filters.values()))
class TemplateCheck(SQLModel):
    folder: str = settings.TEMPLATE_FOLDER
    context_processors: list[str] = CONTEXT_PROCESSORS
    filters: list[str] = FILTERS

class HealthCheck(SQLModel):
    if settings.DEV_MODE is True:
        settings: Settings | None = settings
    template: TemplateCheck = TemplateCheck()
    database: DatabaseCheck = DatabaseCheck()


@router.get("/json")
async def json_health_check():
    return HealthCheck()

@router.get("/web")
async def html_health_check(request: Request):
    context = dict(
        request=request,
        health=HealthCheck(),
    )
    return templates.TemplateResponse(
        name="config_table.html",
        context=context,
    )