from beanie import PydanticObjectId
from pydantic import BaseModel, Field, field_serializer

from app.schemas.base import BaseSchema


class AuthLogResponse(BaseSchema):
    id: PydanticObjectId = Field(...)

    user_id: int
    institution_id: int
    institution_name: str
    location: str
    is_success: bool
    auth_type: str = Field(...)

    @field_serializer("id")
    def serialize_objectid(self, oid: PydanticObjectId, _info):
        return str(oid)

    model_config = {
        "populate_by_name": True,  # alias('_id') → id 변환 허용
        "arbitrary_types_allowed": True,  # PydanticObjectId 허용
        "from_attributes": True,
    }


class VerificationSummaryResponse(BaseModel):
    total_users: int = Field(..., description="전체 유저 수")
    registered_palms: int = Field(..., description="등록된 손바닥 수")
    total_verifications: int = Field(..., description="총 인증 요청 수")
    success_rate: float = Field(..., description="인증 성공률 (%)")
