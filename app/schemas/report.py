from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


# -----------------
# 요청 DTO (Request)
# -----------------
class ReportCreate(BaseModel):
    reason: str = Field(..., description="신고 사유")


class ReportUpdate(BaseModel):
    status: str = Field(
        ..., max_length=50, description="변경할 상태 (pending / approved / rejected)"
    )


# -----------------
# 응답 DTO (Response)
# -----------------
class ReportResponse(BaseSchema):
    user_id: int
    auth_log_id: int
    report_type: str
    description: str
    status: str
