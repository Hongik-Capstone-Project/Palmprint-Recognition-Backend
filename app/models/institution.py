# app/models/institution.py
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, IntPKMixin, TimestampMixin

if TYPE_CHECKING:
    # 여기에 필요한 모델들 다 import
    from .device import Device
    from .user_institution import UserInstitution
    from .user_institution_role import UserInstitutionRole


class Institution(IntPKMixin, TimestampMixin, Base):
    __tablename__ = "institutions"

    name: Mapped[str] = mapped_column(String(255), unique=True)
    address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Relationships
    user_institutions: Mapped[list["UserInstitution"]] = relationship(
        back_populates="institution"
    )
    user_institution_roles: Mapped[list["UserInstitutionRole"]] = relationship(
        back_populates="institution"
    )
    devices: Mapped[list["Device"]] = relationship(back_populates="institution")
