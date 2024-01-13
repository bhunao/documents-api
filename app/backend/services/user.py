from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlmodel import Session

from ..services.base import BaseService
from ..models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


class UserService(BaseService):
    def __init__(
            self,
            session: Session
    ) -> None:
        self.context = pwd_context
        super().__init__(User, session)

    def create(self, new_entry: User) -> User:
        new_entry.password = pwd_context.hash(new_entry.password)
        return super().create(new_entry)

    def authenticate_user(self, username: str, password: str):
        user = self.search(User.username == username)
        if len(user) < 1 or user is None:
            raise credentials_exception
        user = user[0]
        if not self.context.verify(password, user.password):
            return False
        return user
