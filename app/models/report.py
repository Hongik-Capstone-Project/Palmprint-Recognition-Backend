# app/models/report.py
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, IntPKMixin, TimestampMixin

if TYPE_CHECKING:
    from .user import User


class Report(Base, IntPKMixin, TimestampMixin):
    __tablename__ = "reports"

    # Foreign Key (FK) 설정
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    auth_log_id: Mapped[str] = mapped_column(String(50), index=True)

    report_type: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="pending")

    # Relationships
    user: Mapped["User"] = relationship(back_populates="reports")
    # auth_log: Mapped["AuthLog"] = relationship(back_populates="report") # 1:1 관계일 경우 List 없음
