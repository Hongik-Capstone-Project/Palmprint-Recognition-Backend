from datetime import datetime
from decimal import Decimal

from pydantic import Field, field_serializer

from app.schemas.base import BaseSchema
from app.schemas.objectid import PyObjectId


class PaymentHistoryResponse(BaseSchema):
    id: PyObjectId = Field(...)

    user_id: int
    payment_method_id: int
    amount: Decimal = Field(..., decimal_places=2)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @field_serializer("id")
    def serialize_objectid(self, oid: PyObjectId, _info):
        return str(oid)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "from_attributes": True,
    }
