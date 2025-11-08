from fastapi import APIRouter, status

router = APIRouter(prefix="/api/admin/verifications", tags=["Admin-Verifications"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_verifications():
    pass


@router.get("/{verification_id}", status_code=status.HTTP_200_OK)
async def get_verification_detail(verification_id: int):
    pass
