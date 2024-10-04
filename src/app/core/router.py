import logging
from app.core.main import templates
from fastapi import APIRouter, Request

from app.core.schemas import HealthCheck
from app.models import Connection


log = logging.getLogger(__name__)


router = APIRouter(
    prefix="/core",
    tags=["core"],
    dependencies=None # TODO: add user previlege to acess thiss
)

@router.get("/json")
async def json_health_check():
    log.debug(f"connection: {Connection()}")
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
