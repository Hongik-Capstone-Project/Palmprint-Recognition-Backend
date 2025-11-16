# app/models/user_institution_role.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from app.models.base import Base 
from .role import Role 
from .user import User
from .institution import Institution

class UserInstitutionRole(Base):
    __tablename__ = "user_institution_roles"
    
    # Foreign Key (FK) 설정
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    institution_id: Mapped[int] = mapped_column(ForeignKey("institutions.id"), index=True)
    
    # Relationships
    role: Mapped["Role"] = relationship(back_populates="user_institution_roles")
    user: Mapped["User"] = relationship(back_populates="user_institution_roles")
    institution: Mapped["Institution"] = relationship(back_populates="user_institution_roles")
    
    # 복합 유니크 제약 조건 (id2, id3, id4에 해당하는 복합 키 역할)
    __table_args__ = (
        UniqueConstraint('role_id', 'user_id', 'institution_id', name='uix_user_inst_role'),
    )