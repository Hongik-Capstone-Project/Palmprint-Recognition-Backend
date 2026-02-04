from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema

# -----------------
# 요청 DTO (Request)
# -----------------


class UserPalmRegister(BaseModel):
    palmprint_data: str = Field(..., description="Base64 encoded palm image")


class PalmprintVerifyRequest(BaseModel):
    device_id: str = Field(..., description="단말기 고유 ID")
    institution: str = Field(..., description="단말기가 속한 기관명/코드")
    palmprint_data: str = Field(..., description="촬영된 손바닥 데이터 (Base64)")
    auth_type: str = Field(
        ..., description="entry | payment | library | cafeteria | etc"
    )


# -----------------
# 응답 DTO (Response)
# -----------------


class UserPalmResponse(BaseSchema):
    user_id: int
    registered_at: datetime = Field(alias="created_at")
    updated_at: Optional[datetime] = None

    class Config:
        populate_by_name = True


class UserPalmListResponse(BaseModel):
    palms: list[UserPalmResponse]
    total_count: int = Field(description="등록된 손바닥 개수")


class UserPalmRegisterResponse(BaseSchema):
    user_id: int
    registered_at: datetime = Field(alias="created_at")
    message: str = Field(default="Palm registered successfully")


# -----------------
# 내부 사용 DTO
# -----------------


class EmbeddingServiceRequest(BaseModel):
    base64_image: str


class EmbeddingServiceResponse(BaseModel):
    embedding: list[float] = Field(..., description="600차원 벡터")


class PalmMatchResult(BaseModel):
    matched: bool
    user_id: Optional[int] = None
    similarity_score: Optional[float] = None
    palm_id: Optional[int] = None

    class Config:
        frozen = True
