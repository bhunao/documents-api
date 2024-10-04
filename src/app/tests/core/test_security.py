from random import choices
from string import ascii_letters

from app.core.security import get_password_hash, verify_password


def random_str():
    return "".join(choices(ascii_letters, k=25))


def test_hash_password():
    password = random_str()
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password)
