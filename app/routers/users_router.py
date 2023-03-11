from fastapi import Depends, status
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users_model import User
from app.services.users_service import user_crud
from app.commons.dependencies import get_current_user, get_async_db
from app.schemas.users_schema import (
    UserCreateSchema,
    UserUpdateSchema,
    LoginSchema,
    UserOutSchema,
    PasswordSchema,
)

router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
        login_schema: LoginSchema,
        db: AsyncSession = Depends(get_async_db)
):
    return await user_crud.authenticate_user(
        email=login_schema.email,
        password=login_schema.password,
        db=db
    )


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
        register_schema: UserCreateSchema,
        db: AsyncSession = Depends(get_async_db)
):
    return await user_crud.create(user_in=register_schema, db=db)


@router.get(
    path="/user",
    status_code=status.HTTP_200_OK,
    response_model=UserOutSchema
)
async def get_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/user", status_code=status.HTTP_200_OK)
async def update_user(
        user_in: UserUpdateSchema,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db),
):
    return await user_crud.update(user_in, db, current_user)


@router.delete("/user", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db),
):
    return await user_crud.delete(current_user.id, db)


@router.post("/password-change", status_code=status.HTTP_200_OK)
async def change_user_password(
        passwrd_schema: PasswordSchema,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db),
):
    return await user_crud.change_password(current_user.id, db, passwrd_schema)
