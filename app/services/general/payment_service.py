from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.models.payment_method import PaymentMethod
from app.repositories.payment_method_repository import PaymentMethodRepository
from app.schemas.payment_method import PaymentMethodCreate


class PaymentService:
    def __init__(self, session: Session, payment_method_repo: PaymentMethodRepository):
        self.session = session
        self.payment_method_repo = payment_method_repo

    async def get_payment_methods(self, payload: dict) -> list[PaymentMethod]:
        result = await self.session.execute(
            self.payment_method_repo.get_by_user_query(payload["user"]["id"])
        )
        return result.scalars().all()

    async def add_payment_method(
        self, payload: dict, payment_data: PaymentMethodCreate
    ) -> PaymentMethod:
        try:
            payment_method = PaymentMethod(
                user_id=payload["user"]["id"],
                card_name=payment_data.card_name,
                card_id=payment_data.card_id,
            )
            self.session.add(payment_method)
            await self.session.commit()
            await self.session.refresh(payment_method)
            return payment_method
        except Exception:
            await self.session.rollback()
            raise

    async def delete_payment_method(
        self, payload: dict, payment_method_id: int
    ) -> None:
        result = await self.session.execute(
            self.payment_method_repo.get_by_id_and_user_query(
                payment_method_id, payload["user"]["id"]
            )
        )
        payment_method = result.scalar_one_or_none()

        if not payment_method:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="payment_method not found",
            )

        try:
            await self.session.delete(payment_method)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
