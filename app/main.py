from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

import json

from app import authentication, settings
from app.authentication import get_current_active_user

from . import crud, schemas
from .database import create_db_and_tables, get_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    print('...end')

app = FastAPI(
    title=settings.TITLE,
    lifespan=lifespan
)


@app.post("/login", response_model=authentication.Token)
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Session = Depends(get_session)
):
    user = authentication.authenticate_user(
        session,
        form_data.username,
        form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authqwertyenticate": "Bearer"}
        )
    access_token = authentication.create_access_token(
        data={"sub": user.email},
        expires_delta=authentication.ACCESS_TOKEN_EXPIRES
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=schemas.User)
def read_me(
        current_user: Annotated[schemas.User, Depends(get_current_active_user)]
):
    return current_user


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
