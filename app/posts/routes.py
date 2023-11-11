from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.posts.models import Post
from app.users.domain import get_current_active_user

from . import domain, schemas


router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


@router.post("/", response_model=schemas.Post)
def create_post(
        post: schemas.PostCreate,
        current_user: Annotated[schemas.User,
                                Depends(get_current_active_user)],
        session: Session = Depends(get_session)
):
    post_module = domain.PostDomain(session=session, current_user=current_user)
    new_post = post_module.create(post)
    return new_post


@router.get("/all", response_model=list[schemas.Post])
def read_all_posts(
        skip: int = 0,
        limit: int = 100,
        session: Session = Depends(get_session)
):
    post_module = domain.PostDomain(session=session)
    posts = post_module.read_all(skip=skip, limit=limit)
    return posts


@router.get("/{id}", response_model=schemas.Post)
def read_post(
    id: int,
    current_user: Annotated[schemas.User,
                            Depends(get_current_active_user)],
    session: Session = Depends(get_session)
):
    post_module = domain.PostDomain(session=session, current_user=current_user)
    post = post_module.read(Post.id == id)
    return post


@router.put("/{id}")
def update_post(
        id: int,
        new_post: schemas.PostCreate,
        current_user: Annotated[schemas.User,
                                Depends(get_current_active_user)],
        session: Session = Depends(get_session)
):
    post_module = domain.PostDomain(session=session, current_user=current_user)
    post = post_module.update(id, new_post)
    return post


@ router.delete("/{id}")
def delete_post(
    id: int,
    current_user: Annotated[schemas.User,
                            Depends(get_current_active_user)],
    session: Session = Depends(get_session)
):
    post_module = domain.PostDomain(session=session, current_user=current_user)
    deleted = post_module.delete(id)
    return {"deleted": deleted}
