# app/schemas/role.py
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema

# -----------------
# 요청 DTO (Request)
# -----------------


class RoleCreate(BaseModel):
    name: str = Field(..., max_length=100)


# -----------------
# 응답 DTO (Response)
# -----------------


class RoleResponse(BaseSchema):
    name: str
