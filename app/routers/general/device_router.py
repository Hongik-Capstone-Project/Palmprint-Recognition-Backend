from fastapi import APIRouter, status

router = APIRouter(prefix="/api/devices", tags=["Devices"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_devices():
    pass


@router.post("/verify", status_code=status.HTTP_200_OK)
async def request_verification():
    pass
