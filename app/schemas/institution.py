from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema

# -----------------
# 요청 DTO (Request)
# -----------------


class InstitutionCreate(BaseModel):
    name: str = Field(..., max_length=255)
    address: Optional[str] = Field(None, max_length=255)


# -----------------
# 응답 DTO (Response)
# -----------------


class InstitutionResponse(BaseSchema):
    name: str
    address: Optional[str]
