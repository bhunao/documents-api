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


@app.post("/login", tags=["authentication"], response_model=authentication.Token)
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Session = Depends(get_session)
):
    user = users.domain.authenticate_user(
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
        data={"sub": user.username},
        expires_delta=settings.ACCESS_TOKEN_EXPIRES
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/signin", tags=["authentication"], response_model=users.schemas.User)
def create_user(
        user: users.schemas.UserCreate,
        session: Session = Depends(get_session)
):
    db_user = users.domain.read_by_username(session=session, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username already registered")
    return users.domain.create_user(session=session, user=user)


openapi_schema = get_openapi(
    title="App",
    version="0.1.0",
    description="Template FASTAPI app",
    routes=app.routes
)
with open("openapi.yaml", "w") as file:
    file.write(json.dumps(openapi_schema))
