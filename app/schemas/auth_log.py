# app/schemas/auth_log.py

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, field_serializer

from app.schemas.base import BaseSchema
from app.schemas.objectid import PyObjectId
from app.schemas.user_institution import UserInstitutionResponse


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
# 2. user 인증 로그 리스트 
# ---------------------------------------------------------

# 일반 user 인증 내역 조회
class AuthLogItemResponse(BaseSchema): 
    log_id: PyObjectId = Field(alias="_id")
    user_id: Optional[int] = Field(None, description="유저 ID (실패 시 없을 수 있음)")
    device_id: str
    institution: str
    auth_type: str
    result: str = Field(..., alias="is_success")
    timestamp: datetime = Field(..., alias="created_at")

    @field_serializer("log_id")
    def serialize_objectid(self, oid: PyObjectId, _info):
        return str(oid)

    model_config = {
        "populate_by_name": True,  # alias('_id') → id 변환 허용
        "arbitrary_types_allowed": True,  # PyObjectId 허용
        "from_attributes": True,
    }

# 일반 user 인증 내역 조회 응답
class AuthLogDataResponse(BaseModel):
    user_id: str
    verifications: List[AuthLogItemResponse] = Field(default_factory=list) 
    page: int
    size: int
    total: int
    pages: int
    next: Optional[str]
    previous: Optional[str]

# 일반 user 인증 내역 API 전체 응답
class AuthLogAPIResponse(BaseModel):
    status: str
    data: AuthLogDataResponse


# ---------------------------------------------------------
# 3. 관리자 인증 내역 조회 (하단 테이블)
# ---------------------------------------------------------

class AdminVerificationItemResponse(BaseModel):
    user_id: int
    institution_name: str
    location: str
    is_success: bool

class AdminVerificationListResponse(BaseModel):
    items: List[AdminVerificationItemResponse]
    total: int
    page: int
    size: int
    pages: int



