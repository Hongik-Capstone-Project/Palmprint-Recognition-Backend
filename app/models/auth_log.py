from datetime import datetime

from beanie import Document
from bson import ObjectId
from pydantic import Field


class AuthLog(Document):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    user_id: int = Field(...)
    institution_name: str = Field(...)
    location: str = Field(...)
    is_success: bool = Field(...)
    auth_type: str = Field(...)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "auth_logs"

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
