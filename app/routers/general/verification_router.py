from fastapi import APIRouter, Depends, status

from app.core import get_current_payload

router = APIRouter(
    prefix="/api/users/me/verifications",
    tags=["Verifications"],
    dependencies=[Depends(get_current_payload)],
)


@router.get("", status_code=status.HTTP_200_OK)
async def get_verifications():
    pass


@router.post("/{log_id}/report", status_code=status.HTTP_201_CREATED)
async def report_verification(log_id: int):
    pass
