from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Role(Base):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(100), unique=True)

    # Relationships
    # 문자열 "UserInstitutionRole"은 SQLAlchemy가 런타임에 해석하고,
    # List["UserInstitutionRole"]은 위 TYPE_CHECKING 블록 덕분에 에디터가 인식함
    user_institution_roles: Mapped[list["UserInstitutionRole"]] = relationship(
        back_populates="role"
    )
