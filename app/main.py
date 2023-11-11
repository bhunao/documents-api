from contextlib import asynccontextmanager
import json
from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session


from app import authentication, settings
from app.database import get_session, create_db_and_tables
from app.posts.routes import router as posts_router
from app.users.domain import UserDomain
from app.users.routes import router as users_router


from app import users


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    assert app is not None
    yield
    print('...end')


app = FastAPI(
    title=settings.TITLE,
    lifespan=lifespan
)
app.include_router(posts_router)
app.include_router(users_router)


