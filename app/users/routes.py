from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.database import get_session
from app.settings import ACCESS_TOKEN_EXPIRES
from app.users.models import User

from . import schemas
from .domain import UserDomain, authenticate_user, create_access_token, get_current_active_user


router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post("/signin", response_model=schemas.User)
def create_user(
        user: schemas.UserCreate,
        session: Session = Depends(get_session)
):
    user_domain = UserDomain(session=session)
    user = user_domain.create(user)
    return user


@router.post("/login", response_model=schemas.Token)
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Session = Depends(get_session)
):
    user = authenticate_user(
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
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=ACCESS_TOKEN_EXPIRES
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.User)
def read_current_user(
    current_user: Annotated[schemas.User,
                            Depends(get_current_active_user)],
    session: Session = Depends(get_session),
):
    user_domain = UserDomain(session, current_user)
    return user_domain.current_user


@router.get("/all", response_model=list[schemas.User])
def read_all_users(
        current_user: Annotated[schemas.User,
                                Depends(get_current_active_user)],
        skip: int = 0, limit: int = 100,
        session: Session = Depends(get_session),
):

    user_domain = UserDomain(session, current_user)
    users = user_domain.read_all(skip, limit)
    return users


@router.get("/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int,
    current_user: Annotated[schemas.User,
                            Depends(get_current_active_user)],
    session: Session = Depends(get_session),
):
    user_domain = UserDomain(session, current_user)
    user = user_domain.read(User.id == user_id)
    return user
