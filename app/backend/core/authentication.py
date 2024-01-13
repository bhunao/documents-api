from datetime import datetime, timedelta, timezone
from typing import Optional
from typing_extensions import Annotated

from fastapi import Depends,  HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session

from .. import schemas, models
from ..services.base import BaseService
from .config import UserConfigs
from .database import get_session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, UserConfigs.SECRET_KEY, algorithm=UserConfigs.ALGORITHM)
    return encoded_jwt


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: Session = Depends(get_session)
):
    try:
        payload = jwt.decode(
            token,
            UserConfigs.SECRET_KEY,
            algorithms=[UserConfigs.ALGORITHM]
        )
        username = payload.get("sub")
        assert isinstance(username, str)
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = BaseService(models.User, session).search(
        models.User.username == token_data.username)
    if len(user) < 1 or user is None:
        raise credentials_exception
    user = user[0]
    return user


async def get_current_active_user(
    current_user: Annotated[models.User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
