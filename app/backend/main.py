import logging
from fastapi import FastAPI, Depends

from sqlmodel import Session

from .core.utils import get_session, lifespan
from .core.base_service import BaseService
from .models import Post


logger = logging.getLogger(__name__)


TITLE = "TITULO"
app = FastAPI(
    title=TITLE,
    lifespan=lifespan
)


@app.get("/")
def read_all(session: Session = Depends(get_session)):
    ppost = BaseService(Post, session)
    result = ppost.read_all()
    return result


@app.post("/new")
def create(session: Session = Depends(get_session), coisa: str = ""):
    post = Post(content=coisa)
    ppost = BaseService(Post, session)
    ppost.create(post)
    return post


@app.get("/new")
def update(session: Session = Depends(get_session), coisa: str = ""):
    post = Post(content=coisa)
    ppost = BaseService(Post, session)
    ppost.create(post)
    return post
