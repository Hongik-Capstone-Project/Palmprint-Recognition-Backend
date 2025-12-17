# app/schemas/user_institution.py
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


# -----------------
# 요청 DTO (Request)
# -----------------
class UserInstitutionCreate(BaseModel):
    institution_name: str
    institution_user_id: str


# -----------------
# 응답 DTO (Response)
# -----------------
class UserInstitutionResponse(BaseSchema):
    id: str
    name: str
    institution_user_id: str
