from fastapi import APIRouter, status

router = APIRouter(prefix="/api/users/me/payment_methods", tags=["Payments"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_payment_methods():
    pass


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_payment_method():
    pass


@router.delete("/{payment_method_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_payment_method(payment_method_id: int):
    pass
