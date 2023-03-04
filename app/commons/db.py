from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from app.commons.config import settings
from app.commons.mixins import TableNameMixin

engine = create_engine(
    url=settings.POSTGRES_URL,
    echo=settings.POSTGRES_ECHO
)
async_engine = create_async_engine(
    url=settings.POSTGRES_URL_ASYNC,
    echo=settings.POSTGRES_ECHO
)

sync_session = sessionmaker(
    bind=engine,
    class_=Session,
    expire_on_commit=False,
    future=True
)
async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    future=True
)

Base = declarative_base(cls=TableNameMixin)
