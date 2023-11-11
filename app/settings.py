import tomllib
from datetime import timedelta

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
import logging


logging.basicConfig()
logging.getLogger('sqlalchemy.engine.Engine').setLevel(logging.ERROR)


with open("app/config.toml", "rb") as file:
    config = tomllib.load(file)

TITLE = config["config"]['title']

SECRET_KEY = config["authentication"]["secret_key"]
ALGORITHM = config["authentication"]["algorithm"]
ACCESS_TOKEN_EXPIRES = timedelta(
    minutes=config["authentication"]["access_token_expires"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
