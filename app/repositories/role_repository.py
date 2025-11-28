from app.models.role import Role

from .base import BaseRepository


class RoleRepository(BaseRepository[Role]):
    def __init__(self):
        super().__init__(Role)

    def get_by_name_query(self, name: str):
        return self.exact_query(Role.name, name)

    def search_by_name_query(self, keyword: str):
        return self.search_query(Role.name, keyword)
