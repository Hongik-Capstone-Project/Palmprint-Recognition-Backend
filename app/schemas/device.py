from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema
from app.schemas.institution import InstitutionResponse


# -----------------
# 요청 DTO (Request)
# -----------------
class DeviceCreate(BaseModel):
    institution_id: int = Field(..., description="기관 ID (FK)")
    location: Optional[str] = Field(None, max_length=255)


class DeviceUpdate(BaseModel):
    institution_id: int = Field(..., description="기관 ID (FK)")
    location: Optional[str] = Field(None, max_length=255)


# -----------------
# 응답 DTO (Response)
# -----------------
class DeviceCreateResponse(BaseSchema):
    institution_id: int
    location: str


class DeviceResponse(BaseSchema):
    institution: InstitutionResponse = Field(default_factory=list)
    location: str
