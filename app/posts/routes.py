from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
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
    result = domain.create(
        session=session,
        post=post,
        user_id=current_user.id
    )
    return result


@router.get("/all", response_model=list[schemas.Post])
def read_all_posts(
        skip: int = 0,
        limit: int = 100,
        session: Session = Depends(get_session)
):
    posts = domain.read_all(session=session, skip=skip, limit=limit)
    return posts


@router.get("/{id}", response_model=schemas.Post)
def read_post(
    id: int,
    current_user: Annotated[schemas.User,
                            Depends(get_current_active_user)],
    session: Session = Depends(get_session)
):
    assert current_user is not None
    post = domain.read(session, id)
    return post


@router.put("/{id}")
def update_post(
        id: int,
        new_post: schemas.PostCreate,
        current_user: Annotated[schemas.User,
                                Depends(get_current_active_user)],
        session: Session = Depends(get_session)
):
    assert current_user is not None
    post = domain.update(session, id, new_post, current_user)
    return post


@ router.delete("/{id}")
def delete_post(
    id: int,
    current_user: Annotated[schemas.User,
                            Depends(get_current_active_user)],
    session: Session = Depends(get_session)
):
    assert current_user is not None
    deleted = domain.delete(session, id, current_user)
    return {"deleted": deleted}
