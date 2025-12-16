# app/models/auth_log.py
from datetime import datetime

from beanie import Document
from bson import ObjectId
from pydantic import Field


class AuthLog(Document):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    device_id: str = Field(...)
    user_id: int = Field(...)
    is_success: bool = Field(...)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    # device를 조회하지 않고 로그 목록을 바로 반환할 수 있도록
    institution_name: str
    location: str

    class Settings:
        name = "auth_logs"

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
