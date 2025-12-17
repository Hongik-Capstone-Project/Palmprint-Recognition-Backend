from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Device(Base):
    __tablename__ = "devices"

    # Foreign Key (FK) 설정
    institution_id: Mapped[int] = mapped_column(
        ForeignKey("institutions.id"), index=True
    )

    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Relationships
    institution: Mapped["Institution"] = relationship(back_populates="devices")
