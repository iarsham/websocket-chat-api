from typing import Any
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, root_validator
from app.models.users_model import UserStatusEnum
from app.commons.exceptions import BACK_EXCEPTION


class BaseUserSchema(BaseModel):
    full_name: str = Field(example="John Wick")
    email: EmailStr = Field(example="John@gmail.com")


class PasswordSchema(BaseModel):
    password: str = Field(
        default=...,
        min_length=8,
        max_length=128,
        example="john123!qaz",
    )
    confirm_password: str = Field(
        default=...,
        min_length=8,
        max_length=128,
        example="john123!qaz"
    )

    @root_validator()
    def validate_password(cls, values: dict[str, Any]):
        if values.get("password") != values.get("confirm_password"):
            raise BACK_EXCEPTION.PASSWORDS_NOT_EQUAL
        return values


class UserCreateSchema(BaseUserSchema, PasswordSchema):
    ...


class UserUpdateSchema(BaseUserSchema):
    ...


class UserOutSchema(BaseModel):
    full_name: str
    email: EmailStr
    status: UserStatusEnum
    updated_at: datetime

    class Config:
        orm_mode = True


class LoginSchema(BaseModel):
    email: EmailStr = Field(example="alex1!@yahoo.com")
    password: str = Field(example="password!123")
