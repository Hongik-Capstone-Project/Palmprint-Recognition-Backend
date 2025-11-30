# app/schemas/auth_log.py

from datetime import datetime
from typing import Optional

from pydantic import Field, field_serializer

from app.schemas.base import BaseSchema
from app.schemas.objectid import PyObjectId


class AuthLogResponse(BaseSchema):
    id: PyObjectId = Field(alias="_id")

    device_id: int
    user_id: Optional[int] = None
    payment_method_id: Optional[int] = None
    is_success: bool
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @field_serializer("id")
    def serialize_objectid(self, oid: PyObjectId, _info):
        return str(oid)

    model_config = {
        "populate_by_name": True,  # alias('_id') → id 변환 허용
        "arbitrary_types_allowed": True,  # PyObjectId 허용
        "from_attributes": True,
    }
