from datetime import datetime, timedelta
from typing import Any
from jose import jwt
from passlib.context import CryptContext
from app.commons.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordManager:

    @staticmethod
    def make_hash_password(password: str):
        return pwd_context.hash(secret=password)

    @staticmethod
    def verify_hash_password(plain_password: str, hash_password: str):
        return pwd_context.verify(secret=plain_password, hash=hash_password)


def create_access_token(_id: str | Any, expire_delta: timedelta = None):
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(
            hours=settings.ACCESS_TOKEN_HOURS_EXPIRE
        )
    to_encode = {"exp": expire, "sub": str(_id)}
    return jwt.encode(to_encode, settings.SECRET_KEY, settings.JWT_ALGORITHM)


pass_manager = PasswordManager()
