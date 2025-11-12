# app/schemas/auth_log.py
from __future__ import annotations
from pydantic import Field
from typing import Optional
from app.schemas.base import BaseSchema

# AuthLog는 생성 시 API로 입력받기보다 서버 로직에서 생성되므로 Create DTO는 생략하거나 단순화
# -----------------
# 응답 DTO (Response)
# -----------------
class AuthLogResponse(BaseSchema):
    device_id: int
    user_id: int
    payment_method_id: int
    is_success: bool
    
    # 💡 Reports는 1:1 관계이며, AuthLog가 생성된 후 Report가 붙을 수 있으므로 Optional
    report: Optional["ReportResponse"] = None