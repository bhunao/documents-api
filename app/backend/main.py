import logging

from fastapi import FastAPI

from .core.utils import lifespan
from .routes import news, users


logger = logging.getLogger(__name__)


TITLE = "WiproXD"
app = FastAPI(
    title=TITLE,
    lifespan=lifespan
)

app.include_router(users.router)
app.include_router(news.router)


@app.get("/")
def test():
    return {"yes": "no"}
