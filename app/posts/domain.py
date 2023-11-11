from typing import List, Optional
from fastapi import HTTPException
from sqlmodel import Session, select

from app.modules.base_module import BaseModule

from . import schemas
from .models import Post
from app.users.models import User

from icecream import ic


class PostDomain(BaseModule):
    def __init__(
            self,
            session: Session,
            current_user: Optional[User] = None
    ) -> None:
        super().__init__(
            model=Post,
            session=session,
        )
        self.current_user = current_user

    def create(self, post: schemas.PostCreate) -> Post:
        new_entry = Post.from_orm(post)
        if self.current_user is None:
            raise HTTPException(
                status_code=404, detail="user not found")
        new_entry.owner_id = self.current_user.id
        self.current_user
        return super().create(new_entry)

    def update(self, id: int, post: schemas.PostCreate) -> Post:
        user = self.current_user
        if user is None:
            raise HTTPException(
                status_code=404, detail="user not found")

        db_post = self.read(self.model.id == id)
        if db_post.owner_id != user.id:
            raise HTTPException(
                status_code=401, detail="this post is not yours")

        return super().update(id, post)

    def delete(self, id: int) -> bool:
        db_post = self.read(self.model.id == id)
        user = self.current_user
        if user is not None and not db_post.owner_id == user.id:
            raise HTTPException(
                status_code=401, detail="this post is not yours")
        return super().delete(id)
