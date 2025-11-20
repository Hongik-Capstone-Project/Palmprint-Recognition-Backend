# app/schemas/user.py

from __future__ import annotations  # 💡 추가: 관계 모델 참조를 위해 필요

from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from app.schemas.base import BaseSchema

from .payment_method import PaymentMethodResponse
from .report import ReportResponse

# 💡 추가: User와 관계를 맺고 있는 DTO 클래스들을 불러옵니다.
from .user_institution import UserInstitutionResponse
from .user_institution_role import UserInstitutionRoleResponse

# -----------------
# 요청 DTO (Request)
# -----------------


class UserCreate(BaseModel):
    email: EmailStr = Field(..., max_length=255)
    password: str = Field(..., min_length=8)
    name: str = Field(..., max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, max_length=255)
    name: Optional[str] = Field(None, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)
    # 비밀번호 변경은 보통 별도의 DTO를 사용


# -----------------
# 응답 DTO (Response)
# -----------------


class UserResponse(BaseSchema):
    email: str
    name: str
    phone_number: Optional[str]

    # 💡 ODM으로 전환된 클래스(AuthLog, PaymentHistory) 관계는 제거했습니다.
    # 💡 RDB에 남아있는 관계 필드 추가 (List[다른 DTO 클래스])
    payment_methods: List[PaymentMethodResponse] = Field(default_factory=list)
    reports: List[ReportResponse] = Field(default_factory=list)
    user_institutions: List[UserInstitutionResponse] = Field(default_factory=list)
    user_institution_roles: List[UserInstitutionRoleResponse] = Field(
        default_factory=list
    )
