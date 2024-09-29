import logging
from typing import TypeVar


from sqlmodel import SQLModel as SQLModel
from sqlmodel import select, Session

from sqlmodel import create_engine

from src.core.config import (
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_SERVER,
    POSTGRES_DB,
    POSTGRES_PORT,
)


logger = logging.getLogger(__name__)

postgre_url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(postgre_url, echo=False)


class BaseDatabase:
    def __init__(self, session: Session):
        self.session: Session = session

    def create(self, record: SQLModel, table: SQLModel = None) -> SQLModel:
        table = table if table else record.__class__

        new_record = table.model_validate(record, from_attributes=True)
        self.session.add(new_record)
        self.session.commit()
        self.session.refresh(new_record)
        logger.debug(
            f"Record {table.__name__}(id={new_record.id}) created.")
        return new_record

    def read(self, table: SQLModel, id: int) -> SQLModel | None:
        db_record = self.session.get(table, id)
        return db_record

    def read_all(
            self,
            table: SQLModel = None,
            skip: int = 0,
            limit: int = 100
    ) -> list[SQLModel]:
        query = select(table).offset(skip).limit(limit)
        result = self.session.exec(query).all()
        return result

    def update(self, record: SQLModel, table: SQLModel = None) -> SQLModel | None:
        table = table if table else record.__class__
        db_record = self.session.get(table, record.id)
        if db_record is None:
            return None
        db_record.sqlmodel_update(record)
        self.session.add(db_record)
        self.session.commit()
        self.session.refresh(db_record)
        return db_record

    def delete(self, table: SQLModel, id: int) -> SQLModel | None:
        db_record = self.session.get(table, id)
        if db_record is None:
            return None
        self.session.delete(db_record)
        self.session.commit()
        logger.debug(
            f"Record {table.__name__}(id={db_record.id}) deleted.")
        return db_record
