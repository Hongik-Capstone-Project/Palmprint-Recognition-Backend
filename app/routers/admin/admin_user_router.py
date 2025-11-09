from fastapi import APIRouter, status

router = APIRouter(prefix="/api/admin/users", tags=["Admin-Users"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_users():
    pass


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_detail(user_id: int):
    pass


@router.post("/{user_id}", status_code=status.HTTP_200_OK)
async def register_user(user_id: int):
    pass


@router.patch("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: int):
    pass


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    pass
