import logging

from fastapi import FastAPI, Request

from src import routers
from src.core.dependencies import lifespan


app = FastAPI(lifespan=lifespan)
logger = logging.getLogger(__name__)

print(dir(routers))
for name in dir(routers):
    if name.startswith("__") or name == "asddatabase_test":
        continue
    print(f"{name=}")
    logger.error(f"{name=}")
    _router = getattr(routers, name)
    app.include_router(_router)


@app.get("/", response_class=bool)
async def status_check(request: Request) -> bool:
    return True
