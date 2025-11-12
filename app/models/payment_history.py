# app/models/payment_history.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Decimal, ForeignKey
from app.models.base import Base 

class PaymentHistory(Base):
    __tablename__ = "payment_histories"
    
    # Foreign Key (FK) 설정
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    payment_method_id: Mapped[int] = mapped_column(ForeignKey("payment_methods.id"), index=True)
    
    # Decimal(10, 2) 타입 명시
    amount: Mapped[Decimal] = mapped_column(Decimal(10, 2))
    
    # Relationships
    user: Mapped["User"] = relationship(back_populates="payment_histories")
    payment_method: Mapped["PaymentMethod"] = relationship(back_populates="payment_histories")