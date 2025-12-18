from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    # Foreign Key (FK) 설정
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    card_name: Mapped[str] = mapped_column(String(100))
    card_id: Mapped[str] = mapped_column(String(100))

    # Relationships
    user: Mapped["User"] = relationship(back_populates="payment_methods")
