from jinja2_fragments.fastapi import Jinja2Blocks
from starlette.config import Config


templates = Jinja2Blocks(directory="template/")
config = Config(".env")


class UserConfigs:
    # to get a string like this run:
    # openssl rand -hex 32
    SECRET_KEY = config("SECRET_KEY")
    ALGORITHM = config("ALGORITHM", cast=str)
    ACCESS_TOKEN_EXPIRE_MINUTES = config(
        "ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)

    NAME = "User"
    PREFIX = "/user"
    TAGS = ["users"]


class PostConfigs:
    NAME = "POSTS"
    PREFIX = "/post"
    TAGS = ["posts"]
