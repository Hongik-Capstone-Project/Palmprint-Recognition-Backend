from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


# -----------------
# 요청 DTO (Request)
# -----------------
class UserInstitutionRoleCreate(BaseModel):
    role_id: int = Field(..., description="역할 ID (FK)")
    institution_id: int = Field(..., description="기관 ID (FK)")


# -----------------
# 응답 DTO (Response)
# -----------------
class UserInstitutionRoleResponse(BaseSchema):
    role_id: int
    user_id: int
    institution_id: int
