# app/models/role.py
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, IntPKMixin, TimestampMixin

if TYPE_CHECKING:
    from .user_institution_role import UserInstitutionRole


class Role(Base, IntPKMixin, TimestampMixin):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(100), unique=True)

    # Relationships
    # 문자열 "UserInstitutionRole"은 SQLAlchemy가 런타임에 해석하고,
    # List["UserInstitutionRole"]은 위 TYPE_CHECKING 블록 덕분에 에디터가 인식함
    user_institution_roles: Mapped[list["UserInstitutionRole"]] = relationship(
        back_populates="role"
    )
