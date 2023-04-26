import json
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from api import routes

app = FastAPI()
app.include_router(routes.router)
openapi_schema = get_openapi(
    title="Documents API",
    version="0.1.0",
    description="API for storing and retriving documents in json.",
    routes=app.routes,
)
with open("openapi.yaml", "w") as file:
    file.write(json.dumps(openapi_schema))


@app.get("/", tags=["root"])
async def read_root():
    return {"message": "documents api @bhunao"}
