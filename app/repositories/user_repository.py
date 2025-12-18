from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload

from app.models.user import User
from app.models.user_institution import UserInstitution
from app.models.user_institution_role import UserInstitutionRole

from .base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def _with_relationships(self, stmt):
        return stmt.options(
            selectinload(User.payment_methods),
            selectinload(User.reports),
            selectinload(User.user_institutions).selectinload(
                UserInstitution.institution
            ),
            selectinload(User.user_institution_roles).selectinload(
                UserInstitutionRole.role
            ),
        )

    def get_query(self):
        return self._with_relationships(select(User))

    def get_by_id_query(self, id: int):
        return self._with_relationships(select(User).where(User.id == id))

    def get_by_email_query(self, email: str):
        return self._with_relationships(select(User).where(User.email == email))

    def search_by_name_query(self, keyword: str):
        return self.search_query(User.name, keyword)

    def search_by_email_query(self, keyword: str):
        return self.search_query(User.email, keyword)

    def search_by_phone_query(self, keyword: str):
        return self.search_query(User.phone_number, keyword)

    def delete_by_id_query(self, id: int):
        return delete(User).where(User.id == id)
