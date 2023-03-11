from typing import AsyncGenerator, Generator
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import DBAPIError
from app.commons.db import sync_session, async_session
from app.models.users_model import User
from app.commons.config import settings
from app.services.users_service import user_crud
from app.commons.exceptions import BACK_EXCEPTION

oauth_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/access-token")


def get_db() -> Generator[Session, None, None]:
    with sync_session() as db:
        try:
            yield db
            db.commit()
        except DBAPIError:
            db.rollback()
        finally:
            db.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as db:
        try:
            yield db
            await db.commit()
        except DBAPIError:
            await db.rollback()
        finally:
            await db.close()


async def get_current_user(
        db: AsyncSession = Depends(get_async_db),
        token: str = Depends(oauth_schema),
) -> User:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            [settings.JWT_ALGORITHM],
        )
    except (jwt.JWTError, ValidationError):
        raise BACK_EXCEPTION.WRONG_CREDENTIALS
    user = await user_crud.get_by_id(payload["sub"], db)
    if not user:
        raise BACK_EXCEPTION.USER_NOT_FOUND
    return user


async def get_current_active_user(
        current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_authenticated:
        raise BACK_EXCEPTION.USER_IS_NOT_ACTIVE
    return current_user
