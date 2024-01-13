from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from .. import schemas, models
from ..core.authentication import create_access_token, get_current_active_user
from ..core.config import UserConfigs
from ..core.database import get_session
from ..services.user import UserService


router = APIRouter(
        prefix=UserConfigs.PREFIX,
        tags=UserConfigs.TAGS
        )


@router.post("/signup", response_model=models.User)
async def signup(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
):
    user_info = {
        "username": form_data.username,
        "password": form_data.password
    }

    new_user = models.User(**user_info)
    result = UserService(session).create(new_user)
    return result


@router.post("/signin", response_model=schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
):
    user = UserService(session).authenticate_user(
        form_data.username,
        form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=UserConfigs.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=models.User)
async def read_users_me(
    current_user: Annotated[models.User, Depends(get_current_active_user)]
):
    return current_user
