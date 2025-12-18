from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Report(Base):
    __tablename__ = "reports"

    # Foreign Key (FK) 설정
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    auth_log_id: Mapped[str] = mapped_column(index=True)

    report_type: Mapped[str] = mapped_column(String(100), default="test")
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="pending")

    # Relationships
    user: Mapped["User"] = relationship(back_populates="reports")
