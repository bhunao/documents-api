from collections.abc import Callable
from typing import Any

from app.core.config import settings
from app.core.utils import get_input_type, test_jinja_filter

from starlette.requests import Request
from jinja2_fragments.fastapi import Jinja2Blocks

def app_context(request: Request) -> dict[str, Any]:
    """Add context to the template."""
    assert request
    return {"test": "treco"}


# Templating with Jinja2Blocks
templates: Jinja2Blocks = Jinja2Blocks(
    directory=settings.TEMPLATE_FOLDER,
    context_processors=[app_context],
)

## Filters
template_filters: dict[str, Callable[[Any], Any]] = templates.env.filters
template_filters["input_type"] = get_input_type
template_filters["myfiltro"] = test_jinja_filter

## Globals
template_globals: dict[str, Callable[[Any], Any]] = templates.env.globals
