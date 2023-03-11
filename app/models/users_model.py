from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR, BOOLEAN
from starlette.authentication import BaseUser
from app.commons.db import Base
from app.commons.mixins import UUIDMixin, CreatedUpdatedAtMixin


class UserStatusEnum(Enum):
    verified = True
    unverified = False


class User(Base, UUIDMixin, CreatedUpdatedAtMixin, BaseUser):
    full_name: Mapped[str] = mapped_column(
        VARCHAR(length=150),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        VARCHAR(length=150),
        nullable=False,
        unique=True,
        index=True,
    )
    status: Mapped[bool] = mapped_column(
        BOOLEAN(),
        nullable=False,
        default=UserStatusEnum.unverified.value,
    )
    password_hash: Mapped[str] = mapped_column(
        VARCHAR(1500),
        nullable=False,
    )

    @property
    def display_name(self) -> str:
        return self.full_name

    @property
    def identity(self) -> str:
        return str(self.id)

    @property
    def is_authenticated(self) -> bool:
        return True if self.status else False
