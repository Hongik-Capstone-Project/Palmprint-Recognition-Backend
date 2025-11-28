from app.models.user import User

from .base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_email_query(self, email: str):
        return self.exact_query(User.email, email)

    def search_by_name_query(self, keyword: str):
        return self.search_query(User.name, keyword)

    def search_by_email_query(self, keyword: str):
        return self.search_query(User.email, keyword)

    def search_by_phone_query(self, keyword: str):
        return self.search_query(User.phone_number, keyword)
