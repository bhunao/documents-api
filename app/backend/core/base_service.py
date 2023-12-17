import logging
from typing import Generic, List, TypeVar

from fastapi import HTTPException
from sqlalchemy.sql.elements import BinaryExpression
from sqlmodel import SQLModel, Session, select


logger = logging.getLogger(__name__)

M = TypeVar("M", bound=SQLModel)


class BaseService(Generic[M]):
    def __init__(self, model: M, session: Session) -> None:
        self.model: M = model
        self.session = session
        logger.info(f"BaseModule created with model {model.__name__}")

    def _update_model(self, model: M, update: M) -> None:
        for key, val in update:
            model.__setattr__(key, val)

    def create(self, new_entry: M) -> M:
        db_entry = self.model.from_orm(new_entry)
        self._update_model(db_entry, new_entry)
        self.session.add(new_entry)
        self.session.commit()
        self.session.refresh(new_entry)
        logger.debug(f"new entry added to {self.model.__name__}")
        return new_entry

    def read(self, *where: BinaryExpression) -> M:
        query = select(self.model).where(*where)
        result = self.session.exec(query).one_or_none()

        if result is None:
            logger.error(f"{self.model.__name__} not found")
            raise HTTPException(
                status_code=404, detail=f"{self.model.__name__} not found")

        logger.debug(f"found {self.model.__name__} with id {result.id}")
        return result

    def read_all(self, *where: BinaryExpression, skip: int = 0, limit: int = 100) -> M:
        query = select(self.model).offset(skip).limit(limit)
        result = self.session.exec(query).all()
        logger.debug(f"read {len(result)} lines from {skip} to {skip+limit}")
        return result

    def update(self, id: int, schema: M) -> M:
        db_entry = self.read(self.model.id == id)

        if db_entry is None:
            logger.debug(f"{self.model.__name__} not found")
            raise HTTPException(
                status_code=404, detail=f"{self.model.__name__} not found")

        self._update_model(db_entry, schema)
        self.session.add(db_entry)
        self.session.commit()
        self.session.refresh(db_entry)
        logger.debug(f"{self.model.__name__} with id {id} updated")
        return db_entry

    def delete(self, id: int) -> bool:
        db_entry = self.read(self.model.id == id)
        self.session.delete(db_entry)
        self.session.commit()
        logger.debug(f"{self.model.__name__} with id {id} deleted")
        return True

    def search(self, *where: BinaryExpression) -> List[M]:
        query = select(self.model).where(*where)
        result = self.session.exec(query).all()
        logger.debug(f"search found {len(result)} lines")
        return result
