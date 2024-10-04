import logging
from collections.abc import Generator

from sqlmodel import SQLModel, Session, create_engine, select

from app.core.config import settings


engine = create_engine(str(settings.DATABASE_URI))
logger = logging.getLogger(__name__)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


class BaseDatabase:
    def __init__(self, session: Session):
        self.session: Session = session

    def create(self, record: SQLModel, table: SQLModel | None = None) -> SQLModel:
        _table = table if table else record.__class__
        new_record = _table.model_validate(record, from_attributes=True)
        self.session.add(new_record)
        self.session.commit()
        self.session.refresh(new_record)
        logger.debug(f"Record [{new_record} = ] created.")
        return new_record

    def read(self, table: SQLModel, id: int) -> SQLModel | None:
        db_record = self.session.get(table, id)  # pyright: ignore[reportArgumentType]
        return db_record

    def read_all(
        self, table: SQLModel, skip: int = 0, limit: int = 100
    ) -> list[SQLModel]:
        query = select(table).offset(skip).limit(limit)
        result = self.session.exec(query)
        return result.all()

    def update(self, record: SQLModel) -> SQLModel | None:
        _table = record.__class__
        assert hasattr(_table, "id")
        db_record = self.session.get(_table, record.id)
        if db_record is None:
            return None
        updated_record = db_record.sqlmodel_update(record)
        self.session.add(updated_record)
        self.session.commit()
        self.session.refresh(updated_record)
        return updated_record

    def delete(self, table: SQLModel, id: int) -> SQLModel | None:
        db_record = self.session.get(table, id)  # pyright: ignore[reportArgumentType]
        if db_record is None:
            return None
        self.session.delete(db_record)
        self.session.commit()
        logger.debug(f"Record {table.__name__}(id={db_record.id}) deleted.")
        return db_record
