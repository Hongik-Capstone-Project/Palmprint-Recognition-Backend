# app/schemas/device.py
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


# -----------------
# 요청 DTO (Request)
# -----------------
class DeviceCreate(BaseModel):
    id: Optional[int] = Field(
        None, description="디바이스 DB ID"
    )  # Assuming 'id' in POST is DB ID
    institution_id: int = Field(..., description="기관 ID (FK)")
    location: Optional[str] = Field(None, max_length=255)


# 테스트 돌리느라 추가했습니다.
class DeviceUpdate(BaseModel):
    location: Optional[str] = Field(None, max_length=255)


# -----------------
# 응답 DTO (Response)
# -----------------
# [추가됨] 일반적인 장치 응답 DTO (라우터에서 이걸 찾고 있었음!)
class DeviceResponse(BaseSchema):
    institution_id: int
    location: Optional[str]


# 디바이스 추가 성공 (POST 201)
class DeviceCreateResponse(BaseSchema):
    # BaseSchema가 id, created_at을 포함함
    id: str  # 명세서엔 없지만 생성된 ID 식별을 위해 통상적으로 포함
    institution_name: str
    location: Optional[str]


# -------------------------
# 관리자 API 응답 DTO
# -------------------------


class AdminDeviceListItems(BaseSchema):
    institution_name: str
    location: Optional[str]


class AdminDeviceListResponse(BaseModel):
    items: List[AdminDeviceListItems]
    total: int
    page: int
    size: int
    pages: int


class AdminDeviceDetailResponse(BaseSchema):
    institution_name: str
    location: Optional[str]
