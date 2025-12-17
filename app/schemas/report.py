# app/schemas/report.py
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


# -----------------
# 요청 DTO (Request)
# -----------------
class ReportCreate(BaseModel):
    reason: str = Field(..., description="신고 사유")


class ReportUpdate(BaseModel):
    # 신고 내역 수정 (PATCH)
    # 명세서에 따라 'status'만 변경함

    status: str = Field(
        ..., max_length=50, description="변경할 상태 (pending / approved / rejected)"
    )


# -----------------
# 응답 DTO (Response)
# -----------------


# API 3개 공통 응답 스키마
class ReportResponse(BaseSchema):
    user_id: int
    # auth_log_id: int
    report_type: str
    description: str
    status: str
