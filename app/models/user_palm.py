from datetime import datetime
from typing import Optional

from sqlalchemy import JSON, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class UserPalm(Base):
    """손바닥 정맥 임베딩 정보를 저장하는 엔티티"""

    __tablename__ = "user_palms"

    # Base 클래스에서 id (PK, BIGINT)와 created_at (DATETIME)을 이미 상속받음

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )

    # 600차원 float 배열을 JSON으로 저장
    embedding: Mapped[list[float]] = mapped_column(
        JSON, nullable=False, comment="600차원 float 배열"
    )

    # updated_at은 nullable=True로 설정 (DDL과 동일)
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True, onupdate=datetime.utcnow
    )

    # User와의 N:1 관계 설정
    user: Mapped["User"] = relationship(back_populates="user_palms")

    def __repr__(self) -> str:
        return f"UserPalm(id={self.id!r}, user_id={self.user_id!r})"
