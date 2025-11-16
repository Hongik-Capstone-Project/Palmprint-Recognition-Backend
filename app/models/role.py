# app/models/role.py
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.models.base import Base 

class Role(Base):
    __tablename__ = "roles"
    
    name: Mapped[str] = mapped_column(String(100), unique=True)
    
    # Relationships
    user_institution_roles: Mapped[List["UserInstitutionRole"]] = relationship(back_populates="role")