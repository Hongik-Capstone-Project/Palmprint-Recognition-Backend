from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema
from app.schemas.role import RoleResponse


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
    user_id: int
    role: Optional[RoleResponse] = Field(default=None)
    institution_id: int
