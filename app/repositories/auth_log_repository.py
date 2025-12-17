from app.models.auth_log import AuthLog

from .odm_base import BaseOdmRepository


class AuthLogRepository(BaseOdmRepository[AuthLog]):
    def __init__(self):
        super().__init__(AuthLog)

    async def find_by_user(self, user_id: int) -> list[AuthLog]:
        return await AuthLog.find(AuthLog.user_id == user_id).to_list()

    async def find_by_institution(self, institution_id: int) -> list[AuthLog]:
        return await AuthLog.find(AuthLog.institution_id == institution_id).to_list()

    async def find_by_success(self, is_success: bool) -> list[AuthLog]:
        return await AuthLog.find(AuthLog.is_success == is_success).to_list()

    async def find_recent(self, limit: int = 10) -> list[AuthLog]:
        return await AuthLog.find_all().sort("-created_at").limit(limit).to_list()

    async def count_all(self) -> int:
        return await AuthLog.find_all().count()

    async def count_success(self, is_success: bool) -> int:
        return await AuthLog.find(AuthLog.is_success == is_success).count()

    async def count_distinct_users(self) -> int:
        coll = AuthLog.get_motor_collection()
        cursor = coll.aggregate(
            [
                {"$group": {"_id": "$user_id"}},
                {"$count": "count"},
            ]
        )
        docs = await cursor.to_list(length=1)
        return int(docs[0]["count"]) if docs else 0
