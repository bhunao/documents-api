from typing import Annotated, List, Optional
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt
from sqlmodel import Session, select

from app import settings, database
from app.modules.base_module import BaseModule
from app.settings import pwd_context

from . import domain, models, schemas
from .models import User


CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


class UserDomain(BaseModule):
    def __init__(
            self,
            session: Session,
            current_user: Optional[schemas.User] = None
    ) -> None:
        super().__init__(
            model=User,
            session=session,
        )
        self.current_user = current_user

    def create(self, user: schemas.UserCreate) -> schemas.User:
        new_user = models.User(
            username=user.username,
            hashed_password=pwd_context.hash(user.password)
        )
        new_user = super().create(new_user)
        new_user = schemas.User.from_orm(new_user)
        return new_user

    def authenticate_user(self, username: str, password: str) -> schemas.User | None:
        user = self.read(User.username == username)
        if not user:
            return None
        if not pwd_context.verify(password, user.hashed_password):
            return None
        return user

    async def get_current_user(
            self,
            token: Annotated[str, Depends(settings.oauth2_scheme)],
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
            token_data = schemas.TokenData(username=username)
        except JWTError:
            raise CREDENTIALS_EXCEPTION
        assert token_data.username is not None
        user = self.read_all(User.username == token_data.username)
        if len(user) == 0:
            raise CREDENTIALS_EXCEPTION
        return user[0]

    async def get_current_active_user(self, request: Request) -> schemas.User:
        if self.current_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        if not self.current_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        request.state.current_user = self.current_user
        return self.current_user


def create_access_token(
        data: dict,
        expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt
