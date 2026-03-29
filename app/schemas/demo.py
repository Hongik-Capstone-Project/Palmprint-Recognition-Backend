from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


# -----------------
# 요청 DTO (Request)
# -----------------


class DemoRegisterRequest(BaseModel):
    name: str = Field(..., description="사용자 이름")
    palmprint_data: str = Field(..., description="Base64 encoded palm image")


class DemoVerifyRequest(BaseModel):
    palmprint_data: str = Field(..., description="Base64 encoded palm image")


# -----------------
# 응답 DTO (Response)
# -----------------


class DemoRegisterResponse(BaseSchema):
    user_id: int
    palm_id: int
    name: str
    message: str = Field(default="Demo palm registered successfully")


class DemoVerifyResponse(BaseModel):
    matched: bool
    name: str | None = Field(default=None, description="마스킹된 사용자 이름")
    similarity_score: float | None = None
