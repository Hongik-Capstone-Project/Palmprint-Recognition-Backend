from app.models.device import Device

from .base import BaseRepository


class DeviceRepository(BaseRepository[Device]):
    def __init__(self):
        super().__init__(Device)

    def get_by_institution_query(self, institution_id: int):
        return self.exact_query(Device.institution_id, institution_id)

    def search_by_status_query(self, keyword: str):
        return self.search_query(Device.status, keyword)

    def search_by_firmware_query(self, keyword: str):
        return self.search_query(Device.firmware_version, keyword)
