from fastapi import APIRouter, status

router = APIRouter(prefix="/api/users/me/institutions", tags=["Institutions"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_institutions():
    pass


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_institution():
    pass


@router.delete("/{institution_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_institution(institution_id: int):
    pass
