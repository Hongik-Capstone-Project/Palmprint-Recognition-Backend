# app/models/device.py
from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

from .institution import Institution


class Device(Base):
    __tablename__ = "devices"

    # Foreign Key (FK) 설정
    institution_id: Mapped[int] = mapped_column(
        ForeignKey("institutions.id"), index=True
    )

    firmware_version: Mapped[str] = mapped_column(String(100))
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(50))

    # Relationships
    institution: Mapped["Institution"] = relationship(back_populates="devices")
    # auth_logs: Mapped[list["AuthLog"]] = relationship(back_populates="device")
