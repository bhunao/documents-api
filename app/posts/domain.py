from typing import List
from fastapi import HTTPException
from sqlmodel import Session, select

from . import schemas
from .models import Post


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


def delete_post(session: Session, id: int) -> Post:
    query = select(Post).where(Post.id == id)
    post = session.exec(query).one_or_none()
    if post is None:
        raise HTTPException(status_code=404, detail=f"post with id '{id}' not found")
    session.delete(post)
    session.commit()
    return post
