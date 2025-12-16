# app/schemas/user.py

from __future__ import annotations  # 💡 추가: 관계 모델 참조를 위해 필요

from typing import Optional

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
    is_admin: Optional[bool] = Field(False, description="관리자 여부")


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
    isPalmRegistered: bool = Field(False, description="손금 등록 여부")

    # 💡 ODM으로 전환된 클래스(AuthLog, PaymentHistory) 관계는 제거했습니다.
    # 💡 RDB에 남아있는 관계 필드 추가 (List[다른 DTO 클래스])
    payment_methods: list[PaymentMethodResponse] = Field(default_factory=list)
    reports: list[ReportResponse] = Field(default_factory=list)
    user_institutions: list[UserInstitutionResponse] = Field(default_factory=list)
    user_institution_roles: list[UserInstitutionRoleResponse] = Field(
        default_factory=list
    )


# 💡 명세서에 따르면 유저추가(POST) 응답은 id와 message만 줌
class UserCreateResponse(BaseModel):
    id: int
    name: str


class UserListResponse(BaseSchema):
    id: int
    email: str
    # 유저 목록에서는 아이디와 이메일만 반환
    # name: str
    # phone_number: Optional[str] = None
