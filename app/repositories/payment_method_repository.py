from sqlalchemy import select

from app.models.payment_method import PaymentMethod

from .base import BaseRepository


class PaymentMethodRepository(BaseRepository[PaymentMethod]):
    def __init__(self):
        super().__init__(PaymentMethod)

    def get_by_user_query(self, user_id: int):
        return self.exact_query(PaymentMethod.user_id, user_id)

    def get_by_id_and_user_query(self, id: int, user_id: int):
        return select(PaymentMethod).where(
            PaymentMethod.id == id,
            PaymentMethod.user_id == user_id,
        )
