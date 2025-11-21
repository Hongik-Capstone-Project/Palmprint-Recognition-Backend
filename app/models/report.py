# app/models/report.py
from typing import Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

from .user import User  # 💡 User import 추가


class Report(Base):
    __tablename__ = "reports"

    # Foreign Key (FK) 설정
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    auth_log_id: Mapped[int] = mapped_column(ForeignKey("auth_logs.id"), index=True)

    report_type: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50))

    # Relationships
    user: Mapped["User"] = relationship(back_populates="reports")
    # auth_log: Mapped["AuthLog"] = relationship(back_populates="report") # 1:1 관계일 경우 List 없음
