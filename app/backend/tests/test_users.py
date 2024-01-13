import pytest
from typing import Generator

from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine

from ..core.database import get_session, postgre_url, engine
from ..main import app


# engine = create_engine(postgre_url, echo=False)


def override_get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


@pytest.fixture()
def test_db():
    SQLModel.metadata.create_all(bind=engine)
    yield
    SQLModel.metadata.drop_all(bind=engine)


app.dependency_overrides[get_session] = override_get_session
client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"homepage": True}


def test_wrong_login(test_db):
    response = client.post(
        "/signup",
        json={"username": "treco", "password": "dpfojasd"}
    )
    data = response.json()
    assert response.status_code == 422
    assert data == "algo"
