from datetime import timedelta
from pytest import fixture
from random import randint
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine
from app import crud, main, schemas, authentication
from fastapi.testclient import TestClient


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
    app = main.app
    app.dependency_overrides[main.get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_user(client: TestClient):
    rand_n = randint(0, 999)
    json = {
        "email": f"user{rand_n}@something.like",
        "password": f"password{rand_n}"
    }
    response = client.post("/users/", json=json)
    data = response.json()
    assert response.status_code == 200
    assert data["email"] == json["email"]


def test_login_user(client: TestClient):
    rand_n = randint(0, 999)
    user_json = {
        "email": f"user{rand_n}@something.like",
        "password": f"password{rand_n}"
    }
    response = client.post("/users/", json=user_json)
    data = response.json()
    assert response.status_code == 200
    assert data["email"] == user_json["email"]

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'username': user_json['email'],
        'password': user_json['password'],
    }

    response = client.post("/login", headers=headers, data=data)
    response_data = response.json()

    access_token = authentication.create_access_token(
        data={"sub": user_json['email']},
        expires_delta=authentication.ACCESS_TOKEN_EXPIRES
    )

    assert response.status_code == 200
    assert response_data["token_type"] == "bearer"
    assert response_data["access_token"] == access_token


def test_read_user(session: Session, client: TestClient):
    users = []
    for user in range(10):
        rand_n = randint(0, 999)
        user = schemas.UserCreate(
            email=f"user{rand_n}@something.like",
            password=f"password{rand_n}"
        )
        user = crud.create_user(session, user)
        users.append(user)

    for user in users:
        response = client.get(f"/users/{user.id}/")
        data = response.json()

        assert response.status_code == 200
        assert data['id'] == user.id
        assert data['email'] == user.email


def test_create_post(session: Session, client: TestClient):
    rand_n = randint(0, 999)
    user = schemas.UserCreate(
        email=f"user{rand_n}@something.like",
        password=f"password{rand_n}"
    )
    user = crud.create_user(session, user)
    response = client.get(f"/users/{user.id}/")
    data = response.json()

    assert response.status_code == 200
    assert data['id'] == user.id
    assert data['email'] == user.email

    for _ in range(10):
        json = {
            "title": f"# title n{rand_n}",
            "content": f"content number {rand_n}"
        }
        response = client.post(f"/users/{user.id}/posts/", json=json)
        data = response.json()

        assert response.status_code == 200
        assert data["title"] == json["title"]
        assert data["content"] == json["content"]
        assert data["owner_id"] == user.id
