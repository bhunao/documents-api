from typing import List
from sqlmodel import Session, select

from app import authentication

from . import models, schemas
from .models import User, Post
from app.settings import pwd_context


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
        hashed_password=authentication.pwd_context.hash(user.password)
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


def get_posts(session: Session, skip: int = 0, limit: int = 100) -> List[Post]:
    query = select(Post).offset(skip).limit(limit)
    result = session.exec(query).all()
    return result


def create_user_post(session: Session, post: schemas.PostCreate, user_id: int) -> Post:
    new_post = Post.from_orm(post)
    new_post.owner_id = user_id
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post


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
