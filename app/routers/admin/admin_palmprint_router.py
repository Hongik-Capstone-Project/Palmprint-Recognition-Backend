from fastapi import APIRouter, status

router = APIRouter(prefix="/api/admin/palmprints", tags=["Admin-Palmprints"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_palmprints():
    pass


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_palmprint(user_id: int):
    pass


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_palmprint(user_id: int):
    pass
