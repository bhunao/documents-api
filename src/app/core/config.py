from typing import Any

from pydantic.fields import computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings
from starlette.requests import Request


def app_context(request: Request) -> dict[str, Any]:
    """Add context to the template."""
    return {"test": "treco"}

class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Microservice"

    DEV_MODE: bool = False

    # security
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SECRET_KEY: str = "OkfUZjfT-DEFINITLYATOTALSECUREKEYO_MJFtac50"

    # Templating
    TEMPLATE_FOLDER: str = "templates"

    # Database
    DATABASE_USER: str = "DATABASE_USER"
    DATABASE_PASSWORD: str = "DATABASE_PASSWORD"
    DATABASE_SERVER: str = "DATABASE_SERVER"
    DATABASE_PORT: int = 9999
    DATABASE_DB: str = "DATABASE_DB"

    MONGO_INITDB_ROOT_USERNAME: str = "SECRETUSERNAME"
    MONGO_INITDB_ROOT_PASSWORD: str = "SECRETPASSWORD"

    @computed_field
    @property
    def DATABASE_URI(self) -> MultiHostUrl:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.DATABASE_USER,
            password=self.DATABASE_PASSWORD,
            host=self.DATABASE_SERVER,
            port=self.DATABASE_PORT,
            path=self.DATABASE_DB,
        )


settings = Settings()
