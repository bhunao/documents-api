from jinja2_fragments.fastapi import Jinja2Blocks
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from sqlmodel import Session

from .database import engine as _engine, create_db_and_tables


app = FastAPI()
video_path = Path("kuroko01.mp4")
templates = Jinja2Blocks(directory="templates")
app.mount("/static", StaticFiles(directory="static/"), name="static")


def get_session():
    with Session(_engine) as session:
        yield session


@app.on_event("startup")
def on_startup():
    create_db_and_tables()



@app.get("/full_page")
async def full_page(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "magic_number": 42}
    )


@app.get("/only_content")
async def only_content(request: Request):
    return templates.TemplateResponse(
        "page.html.jinja2",
        {"request": request, "magic_number": 42},
        block_name="content"
    )


@app.get("/htmlvideo", response_class=HTMLResponse)
async def read_root(request: Request):
    return """<!DOCTYPE html>
<html>
    <head>
        <title>FastAPI video streaming</title>
    </head>
    <body>
        <video width="600" controls muted="muted">
            <source src="/video" type="video/mp4" />
        </video>
    </body>
</html>"""


def treco():
    with open(video_path, mode="rb") as file:
        yield from file


@app.get("/video", response_class=FileResponse)
async def video_endpoint():
    return video_path
    # return StreamingResponse(treco(), media_type="video/mp4")
    # return Response(data, status_code=206, headers=headers, media_type="video/mp4")
