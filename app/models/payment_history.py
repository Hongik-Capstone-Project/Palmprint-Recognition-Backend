from datetime import datetime

from beanie import Document
from bson import ObjectId
from pydantic import Field


class PaymentHistory(Document):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    user_id: int = Field(...)
    payment_method_id: int = Field(...)
    amount: float = Field(...)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "payment_histories"

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
