# app/schemas/base.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class BaseSchema(BaseModel):
    # Pydantic V2에서 ORM 모드를 활성화하는 설정
    # 이 설정으로 엔티티 객체(ORM 모델)를 DTO로 바로 변환 가능
    model_config = ConfigDict(
        from_attributes=True, 
        populate_by_name=True
    )
    
    # 모든 응답 스키마가 공통으로 가질 필드 (id, created_at)
    id: Optional[int] = None
    created_at: Optional[datetime] = None