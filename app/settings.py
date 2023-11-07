import tomllib
from datetime import timedelta


with open("config.toml", "rb") as file:
    config = tomllib.load(file)

TITLE = config["config"]

SECRET_KEY = config["authentication"]["secret_key"]
ALGORITHM = config["authentication"]["algorithm"]
ACCESS_TOKEN_EXPIRES = timedelta(minutes=config["authentication"]["access_token_expires"])
