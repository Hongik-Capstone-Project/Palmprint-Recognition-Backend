from fastapi import APIRouter, status

router = APIRouter(prefix="/api/admin/devices", tags=["Admin-Devices"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_devices():
    pass


@router.get("/{device_id}", status_code=status.HTTP_200_OK)
async def get_device_detail(device_id: int):
    pass


@router.post("", status_code=status.HTTP_201_CREATED)
async def register_device():
    pass


@router.patch("/{device_id}", status_code=status.HTTP_200_OK)
async def update_device(device_id: int):
    pass


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(device_id: int):
    pass
