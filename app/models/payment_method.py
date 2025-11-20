# app/models/payment_method.py
from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

from .user import User


class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    # Foreign Key (FK) 설정
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    method_type: Mapped[str] = mapped_column(String(50))
    pg_billing_key: Mapped[str] = mapped_column(String(255))
    pg_customer_key: Mapped[str] = mapped_column(String(255))
    card_nickname: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    last_4_digits: Mapped[str] = mapped_column(String(4))

    # Relationships
    user: Mapped["User"] = relationship(back_populates="payment_methods")
    # payment_histories: Mapped[List["PaymentHistory"]] = relationship(back_populates="payment_method")
    # auth_logs: Mapped[List["AuthLog"]] = relationship(back_populates="payment_method")
