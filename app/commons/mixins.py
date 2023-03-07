import uuid
from datetime import datetime
from sqlalchemy import TIMESTAMP, text, INTEGER
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import (
    declared_attr,
    declarative_mixin,
    mapped_column,
    Mapped
)


@declarative_mixin
class TableNameMixin:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


@declarative_mixin
class AutoIDMixin:
    id: Mapped[INTEGER] = mapped_column(
        INTEGER(),
        autoincrement=True,
        primary_key=True
    )


@declarative_mixin
class UUIDMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
        primary_key=True
    )


@declarative_mixin
class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.current_timestamp(),
        nullable=False
    )


@declarative_mixin
class UpdatedAtMixin:
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.current_timestamp(),
        server_onupdate=func.current_timestamp(),
        nullable=False
    )


@declarative_mixin
class CreatedUpdatedAtMixin(CreatedAtMixin, UpdatedAtMixin):
    ...
