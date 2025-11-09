from fastapi import APIRouter, status

router = APIRouter(prefix="/api/users/me/verifications", tags=["Verifications"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_verifications():
    pass


@router.post("/{log_id}/report", status_code=status.HTTP_201_CREATED)
async def report_verification(log_id: int):
    pass
