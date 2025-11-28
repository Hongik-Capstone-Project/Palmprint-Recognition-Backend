from sqlalchemy import select

from app.models.user_institution import UserInstitution

from .base import BaseRepository


class UserInstitutionRepository(BaseRepository[UserInstitution]):
    def __init__(self):
        super().__init__(UserInstitution)

    def get_by_user_query(self, user_id: int):
        return self.exact_query(UserInstitution.user_id, user_id)

    def get_by_institution_query(self, institution_id: int):
        return self.exact_query(UserInstitution.institution_id, institution_id)

    def get_user_in_institution_query(self, user_id: int, institution_id: int):
        return select(UserInstitution).where(
            UserInstitution.user_id == user_id,
            UserInstitution.institution_id == institution_id,
        )

    def get_by_local_id_query(self, local_id: str):
        return self.exact_query(UserInstitution.local_id, local_id)

    def get_by_student_id_query(self, student_id: str):
        return self.exact_query(UserInstitution.student_id, student_id)

    def search_by_local_id_query(self, keyword: str):
        return self.search_query(UserInstitution.local_id, keyword)

    def search_by_student_id_query(self, keyword: str):
        return self.search_query(UserInstitution.student_id, keyword)
