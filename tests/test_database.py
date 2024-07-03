import pytest

from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine

from src.main import app
from src.core.database import get_session, MODEL
from src.routers.database_test import router as database_test_router

BASE_URL = "/example_model"
sqlite_url = "sqlite:///./db_test.db"
engine = create_engine(
    sqlite_url,
    echo=False,
    connect_args={"check_same_thread": False}
)


def mock_get_session():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_session] = mock_get_session
app.include_router(database_test_router)
client = TestClient(app)


@pytest.fixture
def setup_db():
    MODEL.metadata.create_all(engine)
    yield
    MODEL.metadata.drop_all(engine)


def test_connection(setup_db):
    response = client.get(BASE_URL + "/")
    assert response.status_code == 200
