# app/schemas/payment_history.py

from datetime import datetime
from pydantic import Field, BaseModel
from decimal import Decimal
from typing import Optional

# ObjectId 처리를 위해 위에 생성한 유틸리티 임포트
from app.schemas.objectid import PyObjectId 
from app.schemas.base import BaseSchema

# 응답 DTO: MongoDB Document의 구조를 Pydantic으로 정의
class PaymentHistoryResponse(BaseSchema):
    # MongoDB의 고유 ID (PK).
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    # PaymentHistory는 서버 로직에서 생성되므로, 생성 DTO(Create DTO)는 생략함.

    # PaymentHistory의 필드
    user_id: int # ORM 필드 유지
    payment_method_id: int # ORM 필드 유지
    # 금액 (Decimal 타입은 Pydantic v2에서 Decimal 타입 처리를 지원함)
    amount: Decimal = Field(..., decimal_places=2) 
    created_at: datetime = Field(default_factory=datetime.utcnow) # 생성 시각
    
    # Pydantic 설정을 위한 내부 클래스
    class Config:
        allow_population_by_field_name = True
        json_encoders = {PyObjectId: str}