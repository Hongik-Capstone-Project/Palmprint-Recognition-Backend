from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.core import _get_current_payload
from app.core.database import get_db
from app.repositories.payment_method_repository import PaymentMethodRepository
from app.schemas.payment_method import PaymentMethodCreate, PaymentMethodResponse
from app.services.general import PaymentService

router = APIRouter(
    prefix="/api/users/me/payment_methods",
)


def get_payment_service(session: Session = Depends(get_db)) -> PaymentService:
    return PaymentService(
        session=session, payment_method_repo=PaymentMethodRepository()
    )


@router.get(
    "", status_code=status.HTTP_200_OK, response_model=list[PaymentMethodResponse]
)
async def get_payment_methods(
    payload: dict = Depends(_get_current_payload),
    service: PaymentService = Depends(get_payment_service),
):
    return await service.get_payment_methods(payload)


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=PaymentMethodResponse
)
async def add_payment_method(
    body: PaymentMethodCreate,
    payload: dict = Depends(_get_current_payload),
    service: PaymentService = Depends(get_payment_service),
):
    return await service.add_payment_method(payload, body)


@router.delete("/{payment_method_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_payment_method(
    payment_method_id: int,
    payload: dict = Depends(_get_current_payload),
    service: PaymentService = Depends(get_payment_service),
):
    await service.delete_payment_method(payload, payment_method_id)
    return None
