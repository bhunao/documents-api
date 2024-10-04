import pytest

from collections.abc import Generator

from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    """Fixture to create teste cliente per module."""
    # app.dependency_overrides[get_session] = mock_get_session
    with TestClient(app) as client:
        yield client
