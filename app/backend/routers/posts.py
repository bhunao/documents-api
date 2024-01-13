import logging

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlmodel import Session

from ..services.base import BaseService
from ..core.database import get_session
from ..core.config import templates, PostConfigs

from .. import models, schemas


logger = logging.getLogger(__name__)


MODEL = models.Post

router = APIRouter(
    prefix=PostConfigs.PREFIX,
    tags=PostConfigs.TAGS,
)


@router.get("/", response_class=HTMLResponse)
async def read_all(
        request: Request,
        session: Session = Depends(get_session),
        skip: int = 0,
        limit: int = 15
):
    result = BaseService(MODEL, session).read_all(skip=skip, limit=limit)
    return templates.TemplateResponse(
        "cards/list.html",
        {
            "request": request,
            "items": result
        },
        block_name=None
    )


@router.post("/")
async def create(
        post: schemas.Post,
        session: Session = Depends(get_session)
):
    print(post)
    result = BaseService(MODEL, session).create(post)
    return result
