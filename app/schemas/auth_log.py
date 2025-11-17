# app/schemas/auth_log.py

from datetime import datetime
from typing import Optional
from pydantic import Field, BaseModel

# ObjectId 처리를 위해 위에 생성한 유틸리티 임포트
from app.schemas.objectid import PyObjectId 
from app.schemas.base import BaseSchema # BaseSchema는 기존 DTO 구조를 유지하기 위해 사용

# 응답 DTO: MongoDB Document의 구조를 Pydantic으로 정의
class AuthLogResponse(BaseSchema):
    # MongoDB의 고유 ID (PK).
    # Pydantic에서는 PyObjectId 타입을 사용하고, Field에 alias='id'를 설정해서 
    # MongoDB의 '_id' 필드가 DTO에서는 'id'로 표시되게 함.
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    
    # AuthLog는 서버 로직에서 생성되므로, 생성 DTO(Create DTO)는 생략함.

    # AuthLog의 필드
    device_id: int # 기존 ORM 필드 유지
    user_id: Optional[int] = None # ORM 필드 유지 (NULLable)
    payment_method_id: Optional[int] = None # ORM 필드 유지 (NULLable)
    is_success: bool # ORM 필드 유지
    created_at: datetime = Field(default_factory=datetime.utcnow) # 생성 시각
    
    # Report와의 1:1 관계는 Report 쪽에서 FK를 가지도록 처리하면 되므로, 
    # 이 DTO에서는 불필요한 관계 필드는 제거함.
    
    # Pydantic 설정을 위한 내부 클래스
    class Config:
        # alias로 설정된 '_id' 대신 'id'를 사용해 출력할 수 있게 설정
        allow_population_by_field_name = True
        # ODM의 ObjectId를 JSON으로 변환할 수 있도록 PyObjectId 클래스의 인코더 등록
        json_encoders = {PyObjectId: str}