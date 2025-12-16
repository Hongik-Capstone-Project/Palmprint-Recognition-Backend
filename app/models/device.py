# app/models/device.py
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:  # 타입 검사할 때만 import (순환 참조 방지)
    from .institution import Institution


class Device(Base, TimestampMixin):
    __tablename__ = "devices"

    # 💡 스키마에 맞춰 String ID로 설정
    id: Mapped[str] = mapped_column(String(100), primary_key=True)

    # Foreign Key (FK) 설정
    institution_id: Mapped[int] = mapped_column(
        ForeignKey("institutions.id"), index=True
    )

    # firmware_version: Mapped[str] = mapped_column(String(100))
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(50))

    # Relationships
    institution: Mapped["Institution"] = relationship(back_populates="devices")
    # auth_logs: Mapped[list["AuthLog"]] = relationship(back_populates="device")
