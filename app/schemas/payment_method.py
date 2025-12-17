# app/schemas/payment_method.py
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


# -----------------
# 요청 DTO (Request)
# -----------------
class PaymentMethodCreate(BaseModel):
    card_name: str
    card_id: str


class PaymentMethodUpdate(BaseModel):
    pass


# uvicorn 테스트를 위해 작성한 빈 클래스입니다.


# -----------------
# 응답 DTO (Response)
# -----------------
class PaymentMethodResponse(BaseSchema):
    payment_method_id: Optional[str] = Field(None, alias="id")
    card_name: str
    card_id: str
