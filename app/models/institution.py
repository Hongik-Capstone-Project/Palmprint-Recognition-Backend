# app/models/institution.py
from typing import List, Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

from .device import Device
from .user_institution import UserInstitution
from .user_institution_role import UserInstitutionRole


class Institution(Base):
    __tablename__ = "institutions"

    name: Mapped[str] = mapped_column(String(255), unique=True)
    address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Relationships
    user_institutions: Mapped[List["UserInstitution"]] = relationship(
        back_populates="institution"
    )
    user_institution_roles: Mapped[List["UserInstitutionRole"]] = relationship(
        back_populates="institution"
    )
    devices: Mapped[List["Device"]] = relationship(back_populates="institution")
