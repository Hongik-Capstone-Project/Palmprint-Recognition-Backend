from typing import List

from app.models.payment_history import PaymentHistory

from .odm_base import BaseOdmRepository


class PaymentHistoryRepository(BaseOdmRepository[PaymentHistory]):
    def __init__(self):
        super().__init__(PaymentHistory)

    async def find_by_user(self, user_id: int) -> List[PaymentHistory]:
        return await PaymentHistory.find(PaymentHistory.user_id == user_id).to_list()

    async def find_by_payment_method(self, method_id: int) -> List[PaymentHistory]:
        return await PaymentHistory.find(
            PaymentHistory.payment_method_id == method_id
        ).to_list()

    async def find_by_amount_gte(self, amount: float) -> List[PaymentHistory]:
        return await PaymentHistory.find(PaymentHistory.amount >= amount).to_list()

    async def find_recent(self, limit: int = 10) -> List[PaymentHistory]:
        return (
            await PaymentHistory.find_all().sort("-created_at").limit(limit).to_list()
        )
