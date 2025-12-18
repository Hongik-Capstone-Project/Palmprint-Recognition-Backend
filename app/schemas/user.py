from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.schemas.base import BaseSchema

from .payment_method import PaymentMethodResponse
from .report import ReportResponse
from .user_institution import UserInstitutionResponse
from .user_institution_role import UserInstitutionRoleResponse

# -----------------
# 요청 DTO (Request)
# -----------------


class UserCreate(BaseModel):
    email: EmailStr = Field(..., max_length=255)
    password: str = Field(..., min_length=8)
    name: str = Field(..., max_length=100)


class UserAdminCreate(UserCreate):
    is_admin: bool = Field(False)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, max_length=255)
    name: Optional[str] = Field(None, max_length=100)
    is_admin: bool = Field(False)


# -----------------
# 응답 DTO (Response)
# -----------------


class UserCreateResponse(BaseSchema):
    email: str
    name: str
    phone_number: Optional[str]


class UserResponse(BaseSchema):
    email: str
    name: str
    is_admin: bool = Field(False)
    payment_methods: list[PaymentMethodResponse] = Field(default_factory=list)
    reports: list[ReportResponse] = Field(default_factory=list)
    user_institutions: list[UserInstitutionResponse] = Field(default_factory=list)
    user_institution_roles: list[UserInstitutionRoleResponse] = Field(
        default_factory=list
    )
