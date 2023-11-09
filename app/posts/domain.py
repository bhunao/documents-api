from typing import List, Optional
from fastapi import HTTPException
from sqlmodel import Session, select

from app.modules.base_module import BaseModule

from . import schemas
from .models import Post
from app.users.models import User


class PostDomain(BaseModule):
    def __init__(
            self,
            session: Session,
            current_user: Optional[User] = None
    ) -> None:
        super().__init__(
            model=Post,
            session=session,
            current_user=current_user
        )


def create(session: Session, post: schemas.PostCreate, user_id: int) -> Post:
    new_post = Post.from_orm(post)
    Post.from_orm
    new_post.owner_id = user_id
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post


def read_all(session: Session, skip: int = 0, limit: int = 100) -> List[Post]:
    query = select(Post).offset(skip).limit(limit)
    result = session.exec(query).all()
    return result


def read(session: Session, id: int) -> Post:
    query = select(Post).where(Post.id == id)
    result = session.exec(query).one_or_none()
    if result is None:
        raise HTTPException(status_code=404, detail=f"no post with id '{id}'")
    return result


def update(session: Session, id: int, post: schemas.PostCreate, user: User):
    query = select(Post).where(Post.id == id)
    db_post = session.exec(query).one_or_none()
    if db_post is None:
        raise HTTPException(
            status_code=404, detail=f"post with id '{id}' not found")
    if not db_post.owner_id == user.id:
        raise HTTPException(
            status_code=401, detail="this post is not yours")
    db_post.title = post.title
    db_post.content = post.content
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


def delete(session: Session, id: int, user: User) -> Post:
    query = select(Post).where(Post.id == id)
    post = session.exec(query).one_or_none()
    if post is None:
        raise HTTPException(
            status_code=404, detail=f"post with id '{id}' not found")
    if not post.owner_id == user.id:
        raise HTTPException(
            status_code=401, detail="this post is not yours")
    session.delete(post)
    session.commit()
    return post
