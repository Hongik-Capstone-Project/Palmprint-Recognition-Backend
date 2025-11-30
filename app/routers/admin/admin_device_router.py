from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.core.database import get_db
from app.repositories.device_repository import DeviceRepository
from app.schemas.device import DeviceCreate, DeviceResponse, DeviceUpdate
from app.services.admin.admin_device_service import AdminDeviceService

router = APIRouter(prefix="/api/admin/devices", tags=["Admin-Devices"])


def get_admin_device_service(
    session: Session = Depends(get_db),
    device_repo: DeviceRepository = Depends(DeviceRepository),
):
    return AdminDeviceService(session, device_repo)


@router.get("", response_model=list[DeviceResponse], status_code=status.HTTP_200_OK)
async def get_devices(service: AdminDeviceService = Depends(get_admin_device_service)):
    return await service.get_devices()


@router.get(
    "/{device_id}", response_model=DeviceResponse, status_code=status.HTTP_200_OK
)
async def get_device_detail(
    device_id: int, service: AdminDeviceService = Depends(get_admin_device_service)
):
    return await service.get_device_detail(device_id)


@router.post("", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
async def register_device(
    data: DeviceCreate, service: AdminDeviceService = Depends(get_admin_device_service)
):
    return await service.register_device(data)


@router.patch(
    "/{device_id}", response_model=DeviceResponse, status_code=status.HTTP_200_OK
)
async def update_device(
    device_id: int,
    data: DeviceUpdate,
    service: AdminDeviceService = Depends(get_admin_device_service),
):
    return await service.update_device(device_id, data)


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(
    device_id: int, service: AdminDeviceService = Depends(get_admin_device_service)
):
    await service.delete_device(device_id)
    return None
