# app/schemas/user.py
from pydantic import Field, EmailStr
from typing import Optional, List
from app.schemas.base import BaseSchema

# -----------------
# 요청 DTO (Request)
# -----------------

# 사용자 생성 요청 (클라이언트 -> 서버)
class UserCreate(BaseModel):
    email: EmailStr = Field(..., max_length=255)
    password: str = Field(..., min_length=8)
    name: str = Field(..., max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)

# 사용자 정보 업데이트 요청 (일부 필드만 선택적으로 수정)
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, max_length=255)
    name: Optional[str] = Field(None, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)
    # 비밀번호 변경은 보통 별도의 DTO를 사용

# -----------------
# 응답 DTO (Response)
# -----------------

# 사용자 응답 (PaymentMethods 등 관계는 Response DTO 정의 후 추가)
class UserResponse(BaseSchema):
    email: str
    name: str
    phone_number: Optional[str]
    
    # 💡 비밀번호는 절대 응답에 포함하지 않게 됨
    
# 관계가 포함된 상세 응답을 위한 포워드 레퍼런스
# from __future__ import annotations # 필요 시 사용
# payment_methods: List["PaymentMethodResponse"] = [] # 나중에 추가