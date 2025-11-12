# app/schemas/payment_method.py
from __future__ import annotations
from pydantic import Field
from typing import Optional, List
from app.schemas.base import BaseSchema

# -----------------
# 요청 DTO (Request)
# -----------------
class PaymentMethodCreate(BaseModel):
    user_id: int = Field(..., description="사용자 ID (FK)")
    method_type: str = Field(..., max_length=50)
    pg_billing_key: str = Field(..., max_length=255)
    pg_customer_key: str = Field(..., max_length=255)
    card_nickname: Optional[str] = Field(None, max_length=100)
    last_4_digits: str = Field(..., max_length=4)

class PaymentMethodUpdate(BaseModel):
    method_type: Optional[str] = Field(None, max_length=50)
    card_nickname: Optional[str] = Field(None, max_length=100)

# -----------------
# 응답 DTO (Response)
# -----------------
class PaymentMethodResponse(BaseSchema):
    # FK 필드 (ID는 BaseSchema에 포함)
    user_id: int
    method_type: str
    card_nickname: Optional[str]
    last_4_digits: str
    
    # 💡 보안상 billing_key, customer_key는 응답에 포함하지 않음
    
    # Relationships
    # user: "UserResponse" # 순환 참조 방지를 위해 생략하거나 필요에 따라 상세 Response에만 포함