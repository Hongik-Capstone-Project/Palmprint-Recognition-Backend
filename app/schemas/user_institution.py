# app/schemas/user_institution.py
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


# -----------------
# 요청 DTO (Request)
# -----------------
class UserInstitutionCreate(BaseModel):
    user_id: int = Field(..., description="사용자 ID (FK)")
    institution_id: int = Field(..., description="기관 ID (FK)")
    local_id: str = Field(..., max_length=100)
    student_id: str = Field(..., max_length=100)


# -----------------
# 응답 DTO (Response)
# -----------------
class UserInstitutionResponse(BaseSchema):
    user_id: int
    institution_id: int
    local_id: str
    student_id: str
