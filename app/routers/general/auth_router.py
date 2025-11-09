from fastapi import APIRouter, status

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/login", status_code=status.HTTP_200_OK)
async def login():
    pass


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout():
    pass
