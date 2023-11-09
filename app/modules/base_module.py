from typing import Dict, Generic, List, Optional, TypeVar
from fastapi import HTTPException

from sqlmodel import SQLModel, Session, select

from app.users.models import User


M = TypeVar("M", bound=SQLModel)


class BaseModule(Generic[M]):
    def __init__(
            self,
            model: M,
            session: Session,
            current_user: Optional[User] = None
    ) -> None:
        self._model: M = model
        self._session = session
        self._current: M | None = None
        self._current_user: Optional[User] = current_user

    def create(self, vals: Dict[str, str] | SQLModel) -> M:
        new_entry = self._model.from_orm(vals)
        if self._current_user is None:
            raise HTTPException(
                status_code=404, detail="user not found")
        new_entry.owner_id = self._current_user.id
        self._session.add(new_entry)
        self._session.commit()
        self._session.refresh(new_entry)
        return new_entry

    def read(self, *where) -> M:
        model: M = self._model
        query = select(model).where(*where)
        result = self._session.exec(query).one_or_none()

        if result is None:
            raise HTTPException(
                status_code=404, detail="not found")
        return result

    def read_all(self, skip: int = 0, limit: int = 100) -> M:
        model: M = self._model

        query = select(model).offset(skip).limit(limit)
        result = self._session.exec(query).all()
        return result

    def update(self, id: int, vals: Dict[str, str]) -> M:
        model = self._model
        user = self._current_user

        query = select(model).where(model.id == id)
        db_entry = self._session.exec(query).one_or_none()
        if db_entry is None:
            raise HTTPException(
                status_code=404, detail=f"post with id '{id}' not found")
        if not db_entry.owner_id == user.id:
            raise HTTPException(
                status_code=401, detail="this post is not yours")
        db_entry.from_orm(vals)
        SQLModel.up
        User().update_forward_refs
        self._session.add(db_entry)
        self._session.commit()
        self._session.refresh(db_entry)
        return db_entry

    def delete(self) -> M:
        model = self._model
        query = select(model).where(model.id == id)
        user = self._current_user
        post = self._session.exec(query).one_or_none()

        if user is None:
            raise HTTPException(
                status_code=401, detail="user not found")

        if post is None:
            raise HTTPException(
                status_code=404, detail=f"post with id '{id}' not found")

        if not post.owner_id == user.id:
            raise HTTPException(
                status_code=401, detail="this post is not yours")

        self._session.delete(post)
        self._session.commit()
        return post

    def search(self) -> List[M]: ...
