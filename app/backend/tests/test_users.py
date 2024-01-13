from pytest import fixture
from typing import Generator
from random import randint

from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine

from ..core.database import get_session, engine
from ..main import app


@fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def override_get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_session] = override_get_session
client = TestClient(app)


def test_read_main(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"homepage": True}


def test_create_user(client: TestClient):
    rand_n = randint(0, 999)
    username = f"user{rand_n}"
    password = f"password{rand_n}"
    form_data = f"grant_type=&username={username}&password={password}&scope=&client_id=&client_secret="

    response = client.post(
        "/user/signup",
        data=form_data,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "accept": " application/json"
            }
    )
    data = response.json()
    assert response.status_code == 200
    assert data["username"] == username
    # assert data["password"] == password # TODO: verify hash.
