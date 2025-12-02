from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.models.device import Device
from app.repositories.device_repository import DeviceRepository
from app.schemas.device import DeviceCreate, DeviceUpdate


class AdminDeviceService:
    def __init__(self, session: Session, device_repo: DeviceRepository):
        self.session = session
        self.device_repo = device_repo

    def get_devices_query(self):
        return select(Device)

    async def get_device_detail(self, device_id: int):
        query = self.device_repo.get_by_id_query(device_id)
        result = await self.session.execute(query)
        device = result.scalar_one_or_none()
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        return device

    async def register_device(self, device_data: DeviceCreate):
        device_model = Device(**device_data.model_dump())
        self.session.add(device_model)
        await self.session.commit()
        await self.session.refresh(device_model)
        return device_model

    async def update_device(self, device_id: int, update_data: DeviceUpdate):
        query = self.device_repo.get_by_id_query(device_id)
        result = await self.session.execute(query)
        device = result.scalar_one_or_none()
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")

        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(device, key, value)

        await self.session.commit()
        await self.session.refresh(device)
        return device

    async def delete_device(self, device_id: int):
        query = self.device_repo.get_by_id_query(device_id)
        result = await self.session.execute(query)
        device = result.scalar_one_or_none()
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")

        await self.session.delete(device)
        await self.session.commit()
