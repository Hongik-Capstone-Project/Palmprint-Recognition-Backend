from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema
from app.schemas.institution import InstitutionResponse


# -----------------
# 요청 DTO (Request)
# -----------------
class UserInstitutionCreate(BaseModel):
    institution_id: int = Field(..., description="기관 ID (FK)")
    institution_user_id: str = Field(...)


# -----------------
# 응답 DTO (Response)
# -----------------
class UserInstitutionResponse(BaseSchema):
    institution: Optional[InstitutionResponse] = Field(default=None)
    institution_user_id: str
