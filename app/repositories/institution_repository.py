from sqlalchemy import select

from app.models.device import Device
from app.models.institution import Institution
from app.models.user_institution import UserInstitution

from .base import BaseRepository


class InstitutionRepository(BaseRepository[Institution]):
    def __init__(self):
        super().__init__(Institution)

    def get_by_name_query(self, name: str):
        return self.exact_query(Institution.name, name)

    def search_by_name_query(self, keyword: str):
        return self.search_query(Institution.name, keyword)

    def get_users_query(self, institution_id: int):
        return select(UserInstitution).where(
            UserInstitution.institution_id == institution_id
        )

    def get_devices_query(self, institution_id: int):
        return select(Device).where(Device.institution_id == institution_id)
