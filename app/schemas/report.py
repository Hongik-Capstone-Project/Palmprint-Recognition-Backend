# app/schemas/report.py
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


# -----------------
# 요청 DTO (Request)
# -----------------
class ReportCreate(BaseModel):
    user_id: int = Field(..., description="사용자 ID (FK)")
    # auth_log_id: int = Field(..., description="인증 로그 ID (FK)")
    report_type: str = Field(..., max_length=100, description="신고 유형")
    description: str = Field(..., description="신고 내용")  # Text 도메인
    # status: str = Field(..., max_length=50) 생성시 default 값으로 'pending' 처리 예정


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


# -------------------------
# 관리자 API 응답 DTO
# -------------------------

class AdminReportListItems(ReportResponse):
    pass

class AdminReportListResponse(BaseModel):
    items: List[AdminReportListItems]
    total: int
    page: int
    size: int
    pages: int

class AdminReportDetailResponse(ReportResponse):
    pass
