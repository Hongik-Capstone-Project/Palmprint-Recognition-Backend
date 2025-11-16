# app/schemas/report.py
from __future__ import annotations
from pydantic import Field
from typing import Optional
from app.schemas.base import BaseSchema

# -----------------
# 요청 DTO (Request)
# -----------------
class ReportCreate(BaseModel):
    user_id: int = Field(..., description="사용자 ID (FK)")
    auth_log_id: int = Field(..., description="인증 로그 ID (FK)")
    report_type: str = Field(..., max_length=100)
    description: str # Text 도메인
    status: str = Field(..., max_length=50)

# -----------------
# 응답 DTO (Response)
# -----------------
class ReportResponse(BaseSchema):
    user_id: int
    auth_log_id: int
    report_type: str
    description: str
    status: str