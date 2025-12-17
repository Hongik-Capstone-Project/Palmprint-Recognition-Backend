from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


# -----------------
# 요청 DTO (Request)
# -----------------
class UserInstitutionCreate(BaseModel):
    user_id: int = Field(..., description="사용자 ID (FK)")
    institution_id: int = Field(..., description="기관 ID (FK)")
    institution_user_id: str = Field(...)


# -----------------
# 응답 DTO (Response)
# -----------------
class UserInstitutionResponse(BaseSchema):
    user_id: int
    institution_id: int
    institution_user_id: str
