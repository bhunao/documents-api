from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .core.dependencies import lifespan
from . import routers


TITLE = "WiproXD"
app = FastAPI(
    title=TITLE,
    lifespan=lifespan
)
app.mount("/static", StaticFiles(directory="static/"), name="static")
app.include_router(routers.posts)
app.include_router(routers.users)


@app.get("/")
async def read_all(
):
    return {"homepage": True}
