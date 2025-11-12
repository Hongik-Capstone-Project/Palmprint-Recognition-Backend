# app/schemas/payment_history.py
from __future__ import annotations
from pydantic import Field
from typing import Optional
from decimal import Decimal
from app.schemas.base import BaseSchema

# PaymentHistory는 서버 로직에서 생성되므로 Create DTO는 생략
# -----------------
# 응답 DTO (Response)
# -----------------
class PaymentHistoryResponse(BaseSchema):
    user_id: int
    payment_method_id: int
    amount: Decimal = Field(..., decimal_places=2)