from typing import Any
from jinja2 import Template

from httpx import Response

from fastapi.testclient import TestClient


class TemplateResponse(Response):
    template: Template = Template("")
    context: dict[str, Any] = dict()


def get_response_template(response: Response):
    assert hasattr(response, "template")
    assert isinstance(response.template, Template)  # pyright: ignore[reportAttributeAccessIssue]
    assert hasattr(response, "context")
    assert isinstance(response.context, dict)  # pyright: ignore[reportAttributeAccessIssue]
    return response.template  # pyright: ignore[reportAttributeAccessIssue]


def test_core_json_router(client: TestClient):
    response = client.get("/core/json")
    assert response.status_code == 200

    json = response.json()
    assert json is not None


def test_core_html_router(client: TestClient):
    response = client.get("/core/web")
    assert response.status_code == 200

    template = get_response_template(response)
    assert template.name == "config_table.html"
