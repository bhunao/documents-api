from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.users.domain import CurrentUserAnnotated

from . import domain, schemas


router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


@router.get("/all", response_model=list[schemas.Post])
def read_posts(
        skip: int = 0,
        limit: int = 100,
        session: Session = Depends(get_session)
):
    posts = domain.get_posts(session=session, skip=skip, limit=limit)
    return posts


@router.post("/", response_model=schemas.Post)
def create_post(
        post: schemas.PostCreate,
        current_user: CurrentUserAnnotated,
        session: Session = Depends(get_session)
):
    result = domain.create_user_post(
        session=session,
        post=post,
        user_id=current_user.id
    )
    return result


@router.delete("/{id}")
def delete_post(
    id: int,
    current_user: CurrentUserAnnotated,
    session: Session = Depends(get_session)
):
    assert current_user is not None
    deleted = domain.delete_post(session, id)
    return {"deleted": deleted}
