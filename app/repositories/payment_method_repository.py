from app.models.payment_method import PaymentMethod

from .base import BaseRepository


class PaymentMethodRepository(BaseRepository[PaymentMethod]):
    def __init__(self):
        super().__init__(PaymentMethod)

    def get_by_user_query(self, user_id: int):
        return self.exact_query(PaymentMethod.user_id, user_id)

    def get_by_last4_query(self, last4: str):
        return self.exact_query(PaymentMethod.last_4_digits, last4)

    def search_by_card_last4_query(self, keyword: str):
        return self.search_query(PaymentMethod.last_4_digits, keyword)

    def search_by_billing_key_query(self, keyword: str):
        return self.search_query(PaymentMethod.pg_billing_key, keyword)

    def search_by_customer_key_query(self, keyword: str):
        return self.search_query(PaymentMethod.pg_customer_key, keyword)
