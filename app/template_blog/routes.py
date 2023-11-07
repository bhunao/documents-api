from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import APIRouter, FastAPI, HTTPException, Depends
from fastapi.openapi.utils import get_openapi
from sqlmodel import Session

import json

from app.authentication import get_current_active_user

from . import crud, schemas
from .database import create_db_and_tables, get_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    assert app is not None
    yield
    print('...end')

router = APIRouter(
    prefix="/blog",
    tags=["blog"],
    dependencies=[Depends(get_current_active_user)],
    lifespan=lifespan
)


@router.get("/users/me", response_model=schemas.User)
def read_me(
        current_user: Annotated[schemas.User, Depends(get_current_active_user)]
):
    return current_user


@router.post("/users/", response_model=schemas.User)
def create_user(
        user: schemas.UserCreate,
        session: Session = Depends(get_session)
):
    db_user = crud.get_user_by_email(session=session, email=user.email)
    if db_user:
        raise HTTPException(status=400, detail="Email already registered")
    return crud.create_user(session=session, user=user)


@router.get("/users/", response_model=list[schemas.User])
def read_users(
        skip: int = 0, limit: int = 100,
        session: Session = Depends(get_session)
):
    users = crud.get_users(session=session, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int,
    session: Session = Depends(get_session)
):
    db_user = crud.get_user(session=session, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/users/{user_id}/posts/", response_model=schemas.Post)
def create_post_for_user(
        user_id: int,
        post: schemas.PostCreate,
        session: Session = Depends(get_session)
):
    return crud.create_user_post(session=session, post=post, user_id=user_id)


@router.get("/posts/", response_model=list[schemas.Post])
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
    routes=router.routes,
)
with open("openapi.yaml", "w") as file:
    file.write(json.dumps(openapi_schema))
