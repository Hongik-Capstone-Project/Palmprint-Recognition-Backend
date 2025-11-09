from fastapi import APIRouter, status

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def signup():
    pass


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_me():
    pass
