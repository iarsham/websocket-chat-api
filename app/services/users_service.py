from datetime import timedelta
from typing import Any
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.dialects.postgresql import UUID, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import EmailStr
from app.commons.exceptions import BACK_EXCEPTION
from app.commons.base import BaseCRUD
from app.commons.config import settings
from app.models.users_model import User
from app.commons.utils import (
    pass_manager as passwrd,
    create_access_token,
)
from app.schemas.users_schema import (
    UserCreateSchema,
    UserUpdateSchema,
    PasswordSchema
)

PARAM_TYPE = UUID | str


class UserCRUD(BaseCRUD[User, UserCreateSchema, UserCreateSchema, PARAM_TYPE]):

    async def get_by_email(self, email: EmailStr, db: AsyncSession) -> User:
        query = select(self._model).where(self._model.email == email)
        result = await db.execute(statement=query)
        return result.scalars().first()

    async def get_by_id(self, _id: UUID, db: AsyncSession) -> User:
        query = select(self._model).where(self._model.id == _id)
        result = await db.execute(statement=query)
        return result.scalars().first()

    async def create(self, user_in: UserCreateSchema, db: AsyncSession):
        try:
            user = await self.get_by_email(email=user_in.email, db=db)
            if not user:
                user_dict = user_in.dict()
                user_dict.pop("password"), user_dict.pop("confirm_password")
                query = insert(self._model).values(
                    **user_dict,
                    password_hash=passwrd.make_hash_password(user_in.password)
                )
                await db.execute(statement=query)
                return {"response": "User was created"}
            else:
                raise BACK_EXCEPTION.USER_FOUND_WITH_EMAIL
        except IntegrityError as ie:
            raise ie.orig
        except SQLAlchemyError as se:
            raise se

    async def update(
            self,
            schema_in: UserUpdateSchema | dict[str, Any],
            db: AsyncSession,
            current_user: User,
            param=None,
    ):
        try:
            user = self.get_by_id(current_user.id, db)
            if not user:
                raise BACK_EXCEPTION.WRONG_CREDENTIALS
            return await super().update(current_user.id, schema_in, db)
        except IntegrityError as ie:
            raise ie.orig
        except SQLAlchemyError as se:
            raise se

    async def authenticate_user(
            self,
            email: EmailStr,
            password: str,
            db: AsyncSession
    ):
        user = await self.get_by_email(email=email, db=db)
        if not user:
            raise BACK_EXCEPTION.USER_NOT_FOUND

        if not passwrd.verify_hash_password(password, user.password_hash):
            raise HTTPException(
                detail="Password is incorrect",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        if not user.is_authenticated:
            raise BACK_EXCEPTION.USER_IS_NOT_ACTIVE

        return {
            "access_token": create_access_token(
                user.id,
                timedelta(hours=settings.ACCESS_TOKEN_HOURS_EXPIRE)
            ),
            "type": "bearer"
        }

    async def change_password(
            self,
            user_id: UUID,
            db: AsyncSession,
            passwrd_schema: PasswordSchema,
    ):
        user = await self.get_by_id(_id=user_id, db=db)
        new_password = passwrd.make_hash_password(passwrd_schema.password)
        user.password_hash = new_password
        db.add(user)
        return {"response": "password changed successfully"}


user_crud = UserCRUD(User)
