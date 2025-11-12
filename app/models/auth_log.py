# app/models/auth_log.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, ForeignKey
from app.models.base import Base 

class AuthLog(Base):
    __tablename__ = "auth_logs"
    
    # Foreign Key (FK) 설정
    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    payment_method_id: Mapped[int] = mapped_column(ForeignKey("payment_methods.id"), index=True)
    
    is_success: Mapped[bool] = mapped_column(Boolean)
    
    # Relationships
    device: Mapped["Device"] = relationship(back_populates="auth_logs")
    user: Mapped["User"] = relationship(back_populates="auth_logs")
    payment_method: Mapped["PaymentMethod"] = relationship(back_populates="auth_logs")
    report: Mapped[Optional["Report"]] = relationship(back_populates="auth_log") # 1:1 관계