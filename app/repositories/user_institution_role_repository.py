from sqlalchemy import select

from app.models.user_institution_role import UserInstitutionRole

from .base import BaseRepository


class UserInstitutionRoleRepository(BaseRepository[UserInstitutionRole]):
    def __init__(self):
        super().__init__(UserInstitutionRole)

    def get_by_user_query(self, user_id: int):
        return self.exact_query(UserInstitutionRole.user_id, user_id)

    def get_by_institution_query(self, institution_id: int):
        return self.exact_query(UserInstitutionRole.institution_id, institution_id)

    def get_by_role_query(self, role_id: int):
        return self.exact_query(UserInstitutionRole.role_id, role_id)

    def get_roles_for_user_in_institution_query(
        self, user_id: int, institution_id: int
    ):
        return select(UserInstitutionRole).where(
            UserInstitutionRole.user_id == user_id,
            UserInstitutionRole.institution_id == institution_id,
        )

    def get_users_with_role_query(self, role_id: int):
        return self.exact_query(UserInstitutionRole.role_id, role_id)
