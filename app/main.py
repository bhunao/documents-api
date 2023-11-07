from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

import json

from . import crud, schemas
from .database import engine as _engine, create_db_and_tables


app = FastAPI(
    title="Template Project"
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def decode_token(token: str):
    password = token + "notreallyhashed"
    return schemas.User(email="test@email", hashed_password=password)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = decode_token(token)
    return user


def get_session():
    with Session(_engine) as session:
        yield session


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/me/")
def get_me(current_user: Annotated[schemas.User, Depends(get_current_user)]):
    return current_user


@app.get("/test/")
def test(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"msg": "test", "token": token}


@app.post("/users/", response_model=schemas.User)
def create_user(
        user: schemas.UserCreate,
        session: Session = Depends(get_session)
):
    db_user = crud.get_user_by_email(session=session, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(session=session, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(
        skip: int = 0, limit: int = 100,
        session: Session = Depends(get_session)
):
    users = crud.get_users(session=session, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int,
    session: Session = Depends(get_session)
):
    db_user = crud.get_user(session=session, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/posts/", response_model=schemas.Post)
def create_post_for_user(
        user_id: int,
        post: schemas.PostCreate,
        session: Session = Depends(get_session)
):
    return crud.create_user_post(session=session, post=post, user_id=user_id)


@app.get("/posts/", response_model=list[schemas.Post])
def read_posts(
        skip: int = 0,
        limit: int = 100,
        session: Session = Depends(get_session)
):
    posts = crud.get_posts(session=session, skip=skip, limit=limit)
    return posts


openapi_schema = get_openapi(
    title="App",
    version="0.1.0",
    description="Template FASTAPI app",
    routes=app.routes,
)
with open("openapi.yaml", "w") as file:
    file.write(json.dumps(openapi_schema))
