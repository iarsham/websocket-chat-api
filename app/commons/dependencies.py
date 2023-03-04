from typing import AsyncGenerator, Generator
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import DBAPIError
from app.commons.db import sync_session, async_session


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
