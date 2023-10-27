from typing import List
from sqlalchemy.future import Engine
from sqlmodel import Session, select

from . import models, schemas
from .models import User, Post


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
    query = select(User)
    print("="*50)
    print(query)
    print("="*50)
    result = session.exec(query).all()
    return result


def create_user(session: Session, user: schemas.UserCreate) -> User:
    fake_hashed_password = user.password + "notreallyhashed"
    new_user = models.User(
        email=user.email,
        hashed_password=fake_hashed_password
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
