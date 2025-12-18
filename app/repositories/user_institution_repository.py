from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.user_institution import UserInstitution

from .base import BaseRepository


class UserInstitutionRepository(BaseRepository[UserInstitution]):
    def __init__(self):
        super().__init__(UserInstitution)

    def _with_relationships(self, stmt):
        return stmt.options(
            selectinload(UserInstitution.institution),
        )

    def get_by_user_query(self, user_id: int):
        return self._with_relationships(
            self.exact_query(UserInstitution.user_id, user_id)
        )

    def get_by_user_and_institution_query(self, user_id: int, institution_id: int):
        stmt = select(UserInstitution).where(
            UserInstitution.user_id == user_id,
            UserInstitution.institution_id == institution_id,
        )
        return self._with_relationships(stmt)

    def get_by_institution_user_id_query(self, institution_user_id: str):
        return self._with_relationships(
            self.exact_query(UserInstitution.institution_user_id, institution_user_id)
        )

    def search_by_institution_user_id_query(self, keyword: str):
        return self._with_relationships(
            self.search_query(UserInstitution.institution_user_id, keyword)
        )
