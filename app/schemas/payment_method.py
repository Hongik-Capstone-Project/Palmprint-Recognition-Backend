from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


# -----------------
# 요청 DTO (Request)
# -----------------
class PaymentMethodCreate(BaseModel):
    card_name: str = Field(...)
    card_id: str = Field(...)


class PaymentMethodUpdate(BaseModel):
    card_name: str = Field(...)
    card_id: str = Field(...)


# -----------------
# 응답 DTO (Response)
# -----------------
class PaymentMethodResponse(BaseSchema):
    card_name: str = Field(...)
    card_id: str = Field(...)
