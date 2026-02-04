from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema
from app.schemas.institution import InstitutionResponse
from app.schemas.payment_method import PaymentMethodResponse
from app.schemas.user import UserCreateResponse


# -----------------
# 요청 DTO (Request)
# -----------------
class DeviceCreate(BaseModel):
    institution_id: int = Field(..., description="기관 ID (FK)")
    location: Optional[str] = Field(None, max_length=255)


class DeviceUpdate(BaseModel):
    institution_id: int = Field(..., description="기관 ID (FK)")
    location: Optional[str] = Field(None, max_length=255)


class DeviceVerificationRequest(BaseModel):
    """디바이스 인증 요청"""

    device_id: int = Field(..., description="단말기 고유 ID")
    palmprint_data: str = Field(..., description="촬영된 손바닥 데이터 (Base64)")
    auth_type: str = Field(
        ..., description="entry | payment | library | cafeteria | etc"
    )


# -----------------
# 응답 DTO (Response)
# -----------------
class DeviceCreateResponse(BaseSchema):
    institution_id: int
    location: str


class DeviceResponse(BaseSchema):
    institution: InstitutionResponse = Field(default_factory=list)
    location: str


class DeviceVerificationResponse(BaseModel):
    status: str = Field(default="success")
    user: Optional[UserCreateResponse] = None
    payment_method: Optional[PaymentMethodResponse] = None
