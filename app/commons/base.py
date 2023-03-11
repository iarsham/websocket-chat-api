from typing import Generic, TypeVar, Any, Sequence
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, Row, RowMapping
from sqlalchemy.dialects.postgresql import insert, UUID
from pydantic import BaseModel
from app.commons.db import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)
PathParam = TypeVar("PathParam", bound=UUID)


class BaseCRUD(Generic[ModelType, CreateSchema, UpdateSchema, PathParam]):
    def __init__(self, model):
        self._model = model

    async def get_all(
            self,
            db: AsyncSession,
            offset: int = 0,
            limit: int = 0
    ) -> Sequence[Row | RowMapping | Any]:
        query = select(self._model).order_by(self._model.created_at) \
            .offset(offset).limit(limit)
        result = await db.execute(statement=query)
        return result.scalars().all()

    async def get(self, _id: PathParam, db: AsyncSession) -> ModelType:
        query = select(self._model).where(self._model.id == _id)
        result = await db.execute(statement=query)
        return result.scalars().first()

    async def create(
            self,
            schema_in: CreateSchema,
            db: AsyncSession
    ) -> ModelType:
        obj = jsonable_encoder(schema_in)
        query = insert(self._model).values(**obj)
        await db.execute(statement=query)
        return obj

    async def update(
            self,
            param: PathParam,
            schema_in: UpdateSchema | dict[str, ...],
            db: AsyncSession) -> ModelType:
        obj = jsonable_encoder(schema_in)
        query = update(self._model).where(self._model.id == param) \
            .values(**obj).execution_options(synchronize_session="fetch")
        await db.execute(statement=query)
        return obj

    async def delete(self, param: PathParam, db: AsyncSession):
        query = delete(self._model).where(self._model.id == param) \
            .execution_options(synchronize_session="fetch")
        await db.execute(statement=query)
        return {"response": "Successfully deleted"}
