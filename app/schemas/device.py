# app/schemas/device.py
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


# -----------------
# 요청 DTO (Request)
# -----------------
class DeviceCreate(BaseModel):
    id: int = Field(..., description="Device ID")
    institution_name: str = Field(..., max_length=255, description="기관명")
    # firmware_version: str = Field(..., max_length=100)
    location: Optional[str] = Field(None, max_length=255)
    # status: str = Field(..., max_length=50)


# 명세서와 와이어프레임에는 수정 기능이 없지만 나중에 필요할지 몰라 남겨놨습니다
class DeviceUpdate(BaseModel):
    device_id: str
    institution: str
    palmprint_data: str
    auth_type: str


# -----------------
# 응답 DTO (Response)
# -----------------


# 디바이스 추가, 목록 조회, 상세 조회 (GET Detail)
# 명세서: id, device_id, institution_name, location, created_at
# (목록 조회와 달리 institution_id가 없음)
class DeviceResponse(BaseSchema):
    # BaseSchema가 id, created_at을 포함함
    device_id: int
    institution_name: str
    location: Optional[str]
