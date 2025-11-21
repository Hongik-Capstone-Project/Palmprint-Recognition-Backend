from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

# 순환 참조 방지를 위한 조건부 임포트
# 런타임에는 실행되지 않지만, Pylance 같은 정적 분석 도구는 이 블록을 읽음
if TYPE_CHECKING:
    from app.models.user_institution_role import UserInstitutionRole


class Role(Base):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(100), unique=True)

    # Relationships
    # 문자열 "UserInstitutionRole"은 SQLAlchemy가 런타임에 해석하고,
    # List["UserInstitutionRole"]은 위 TYPE_CHECKING 블록 덕분에 에디터가 인식함
    user_institution_roles: Mapped[List["UserInstitutionRole"]] = relationship(
        back_populates="role"
    )
