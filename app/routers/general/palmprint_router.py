from fastapi import APIRouter, status

router = APIRouter(prefix="/api/users/me/palmprints", tags=["Palmprints"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_palmprint_status():
    pass


@router.post("", status_code=status.HTTP_201_CREATED)
async def register_palmprint():
    pass


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_palmprint():
    pass
