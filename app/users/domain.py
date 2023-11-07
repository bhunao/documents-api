from typing import Annotated, List

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt
from sqlmodel import Session, select

from app import settings, database
from app.settings import pwd_context
from app.authentication import TokenData

from . import domain, models, schemas
from .models import User


# to get a string like this run:
# openssl rand -hex 32
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_user(session: Session, user_id: int) -> User | None:
    query = select(User).where(
        User.id == user_id
    )
    result = session.exec(query).first()
    return result


def get_user_by_email(session: Session, email: str) -> User | None:
    query = select(User).where(
        User.email == email
    )
    result = session.exec(query).first()
    return result


def get_users(session: Session, skip: int = 0, limit: int = 100) -> List[User]:
    query = select(User).offset(skip).limit(limit)
    result = session.exec(query).all()
    return result


def create_user(session: Session, user: schemas.UserCreate) -> User:
    new_user = models.User(
        email=user.email,
        hashed_password=pwd_context.hash(user.password)
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


def authenticate_user(
        session: Session,
        username: str,
        password: str
) -> models.User | None:
    user = get_user_by_email(session, username)
    if not user:
        return None
    if not pwd_context.verify(password, user.hashed_password):
        return None
    return user


async def get_current_user(
        token: Annotated[str, Depends(settings.oauth2_scheme)],
        session: Session = Depends(database.get_session)
) -> models.User:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        username = payload.get("sub")
        if username is None:
            raise CREDENTIALS_EXCEPTION
        token_data = TokenData(username=username)
    except JWTError:
        raise CREDENTIALS_EXCEPTION
    assert token_data.username is not None
    user = domain.get_user_by_email(session, token_data.username)
    if user is None:
        raise CREDENTIALS_EXCEPTION
    return user


async def get_current_active_user(
        current_user: Annotated[schemas.User, Depends(get_current_user)],
        request: Request
) -> schemas.User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    request.state.current_user = current_user
    return current_user


CurrentUserAnnotated = Annotated[
    schemas.User,
    Depends(get_current_active_user)
]