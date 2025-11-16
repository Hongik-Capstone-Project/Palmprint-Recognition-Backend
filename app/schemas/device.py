# app/schemas/device.py
from __future__ import annotations
from pydantic import Field
from typing import Optional, List
from app.schemas.base import BaseSchema

# -----------------
# 요청 DTO (Request)
# -----------------
class DeviceCreate(BaseModel):
    institution_id: int = Field(..., description="기관 ID (FK)")
    firmware_version: str = Field(..., max_length=100)
    location: Optional[str] = Field(None, max_length=255)
    status: str = Field(..., max_length=50)

class DeviceUpdate(BaseModel):
    firmware_version: Optional[str] = Field(None, max_length=100)
    location: Optional[str] = Field(None, max_length=255)
    status: Optional[str] = Field(None, max_length=50)

# -----------------
# 응답 DTO (Response)
# -----------------
class DeviceResponse(BaseSchema):
    institution_id: int
    firmware_version: str
    location: Optional[str]
    status: str