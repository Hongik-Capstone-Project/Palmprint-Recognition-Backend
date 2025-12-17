from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    # Pydantic V2에서 ORM 모드를 활성화하는 설정
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    # 모든 응답 스키마가 공통으로 가질 필드 (id, created_at)
    id: Optional[int] = None
    created_at: Optional[datetime] = None
