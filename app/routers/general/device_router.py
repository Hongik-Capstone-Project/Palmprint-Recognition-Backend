from fastapi import APIRouter, Depends, status

from app.core import _get_current_payload

router = APIRouter(
    prefix="/api/devices",
    tags=["Devices"],
    dependencies=[Depends(_get_current_payload)],
)


# @router.post("/verify", status_code=status.HTTP_200_OK)
# async def request_verification():
#     pass
