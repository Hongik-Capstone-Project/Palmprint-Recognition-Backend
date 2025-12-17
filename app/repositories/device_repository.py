from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.device import Device

from .base import BaseRepository


class DeviceRepository(BaseRepository[Device]):
    def __init__(self):
        super().__init__(Device)

    def _with_relationships(self, stmt):
        return stmt.options(selectinload(Device.institution))

    def get_by_id_query(self, id: int):
        return self._with_relationships(select(Device).where(Device.id == id))

    def get_by_institution_query(self, institution_id: int):
        return self.exact_query(Device.institution_id, institution_id)
