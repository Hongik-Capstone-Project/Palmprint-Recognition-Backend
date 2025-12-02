from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


# User 엔티티 정의
class User(Base):
    __tablename__ = "users"

    # Base 클래스에서 id (PK, BIGINT)와 created_at (DATETIME)을 이미 상속받음

    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True  # 이메일은 중복되면 안 됨
    )

    password: Mapped[str] = mapped_column(String(255))

    name: Mapped[str] = mapped_column(String(100))

    # phone_number는 ERD에 따라 Optional로 설정
    phone_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    # is_active 필드를 추가하여 계정 활성화 여부를 관리할 수 있습니다 (일반적인 관례)
    # is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # 💡 관계 설정 (RelationShips): User가 다른 테이블을 참조하는 관계

    # PaymentMethods와의 1:N 관계 설정
    payment_methods: Mapped[list["PaymentMethod"]] = relationship(back_populates="user")

    # PaymentHistories와의 1:N 관계 설정
    # payment_histories: Mapped[List["PaymentHistory"]] = relationship(back_populates="user")

    # AuthLogs와의 1:N 관계 설정
    # auth_logs: Mapped[List["AuthLog"]] = relationship(back_populates="user")

    # Reports와의 1:N 관계 설정
    reports: Mapped[list["Report"]] = relationship(back_populates="user")

    # UserInstitutions(중간 테이블)과의 M:N 관계를 위한 관계 설정
    user_institutions: Mapped[list["UserInstitution"]] = relationship(
        back_populates="user"
    )

    # UserInstitutionRoles(중간 테이블)과의 M:N 관계를 위한 관계 설정
    user_institution_roles: Mapped[list["UserInstitutionRole"]] = relationship(
        back_populates="user"
    )

    # 기타 다른 관계 설정...

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r})"
