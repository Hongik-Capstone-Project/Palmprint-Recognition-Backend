# app/models/user_institution.py
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, IntPKMixin, TimestampMixin

if TYPE_CHECKING:
    from .institution import Institution
    from .user import User


class UserInstitution(Base, IntPKMixin, TimestampMixin):
    __tablename__ = "user_institutions"

    # 기본 PK id 외에 user_id와 institution_id로 복합 키 설정
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    institution_id: Mapped[int] = mapped_column(
        ForeignKey("institutions.id"), index=True
    )
    local_id: Mapped[str] = mapped_column(String(100))
    student_id: Mapped[str] = mapped_column(String(100))

    # Relationships
    user: Mapped["User"] = relationship(back_populates="user_institutions")
    institution: Mapped["Institution"] = relationship(
        back_populates="user_institutions"
    )

    # 복합 유니크 제약 조건 (id2, id3에 해당하는 복합 키 역할)
    __table_args__ = (
        UniqueConstraint("user_id", "institution_id", name="uix_user_institution"),
    )
