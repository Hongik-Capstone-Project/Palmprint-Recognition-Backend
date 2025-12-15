# app/schemas/device.py
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


# -----------------
# 요청 DTO (Request)
# -----------------
class DeviceCreate(BaseModel):
    device_id: str = Field(
        ..., max_length=100, description="디바이스 식별 ID (예: '11')"
    )
    institution_id: int = Field(..., description="기관 ID (FK)")
    # firmware_version: str = Field(..., max_length=100)
    location: Optional[str] = Field(None, max_length=255)
    # status: str = Field(..., max_length=50)


# 명세서와 와이어프레임에는 수정 기능이 없지만 나중에 필요할지 몰라 남겨놨습니다
class DeviceUpdate(BaseModel):
    device_id: Optional[str] = Field(
        ..., max_length=100, description="디바이스 식별 ID (예: '11')"
    )
    institution_id: Optional[int] = Field(..., description="기관 ID (FK)")
    # firmware_version: Optional[str] = Field(None, max_length=100)
    location: Optional[str] = Field(None, max_length=255)
    # status: Optional[str] = Field(None, max_length=50)


# -----------------
# 응답 DTO (Response)
# -----------------
# 디바이스 추가 성공 (POST 201)
# 명세서: id, institution_name, location, created_at
class DeviceCreateResponse(BaseSchema):
    # BaseSchema가 id, created_at을 포함함
    device_id: str  # 명세서엔 없지만 생성된 ID 식별을 위해 통상적으로 포함
    institution_name: str
    location: Optional[str]


# 디바이스 목록 조회 (GET List)
# 명세서: id, device_id, institution_name, location, created_at, institution_id
class DeviceListResponse(BaseSchema):
    # BaseSchema가 id, created_at을 포함함
    device_id: str
    institution_name: str
    institution_id: int
    location: Optional[str]

    # 💡 명세서 주석에 "status는 화면에 표시되지 않음"이라고 되어 있어 주석 처리
    # status: Optional[str]


# 디바이스 상세 조회 (GET Detail)
# 명세서: id, device_id, institution_name, location, created_at
# (목록 조회와 달리 institution_id가 없음)
class DeviceResponse(BaseSchema):
    # BaseSchema가 id, created_at을 포함함
    device_id: str
    institution_name: str
    location: Optional[str]
