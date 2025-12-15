# app/schemas/auth_log.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_serializer

from app.schemas.base import BaseSchema
from app.schemas.objectid import PyObjectId


# ---------------------------------------------------------
# 1. 상단 통계 요약 정보 (GET /api/admin/verifications/summary)
# ---------------------------------------------------------
# 이 데이터는 집계 결과이므로 ODM 스키마(ObjectId)가 필요 없고 단순 데이터만 전달합니다.
class VerificationSummaryResponse(BaseModel):
    total_users: int = Field(..., description="전체 유저 수")
    registered_palms: int = Field(..., description="등록된 손바닥 수")
    total_verifications: int = Field(..., description="총 인증 요청 수")
    success_rate: float = Field(..., description="인증 성공률 (%)")


# ---------------------------------------------------------
# 2. 하단 인증 로그 리스트 (테이블 표시용)
# ---------------------------------------------------------


class AuthLogResponse(BaseSchema):
    id: PyObjectId = Field(alias="_id")

    # 💡 [와이어프레임 요구사항] 화면 표시 필드
    # 로그 DB(MongoDB)에는 device_id만 있지만,
    # 서비스 계층에서 SQL 조인 후 '기관명'과 '위치'를 채워서 응답해야 합니다.
    user_id: Optional[int] = Field(None, description="유저 ID (실패 시 없을 수 있음)")
    institution_name: str = Field(..., description="기관명 (Device 정보 Join)")
    location: str = Field(..., description="위치 (Device 정보 Join)")
    is_success: bool = Field(..., description="인증 성공 여부")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @field_serializer("id")
    def serialize_objectid(self, oid: PyObjectId, _info):
        return str(oid)

    model_config = {
        "populate_by_name": True,  # alias('_id') → id 변환 허용
        "arbitrary_types_allowed": True,  # PyObjectId 허용
        "from_attributes": True,
    }
