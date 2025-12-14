from typing import List

from app.models.auth_log import AuthLog

from .odm_base import BaseOdmRepository


class AuthLogRepository(BaseOdmRepository[AuthLog]):
    def __init__(self):
        super().__init__(AuthLog)

    async def find_by_user(self, user_id: int) -> List[AuthLog]:
        return await AuthLog.find(AuthLog.user_id == user_id).to_list()

    async def find_by_device(self, device_id: int) -> List[AuthLog]:
        return await AuthLog.find(AuthLog.device_id == device_id).to_list()

    async def find_by_success(self, is_success: bool) -> List[AuthLog]:
        return await AuthLog.find(AuthLog.is_success == is_success).to_list()

    async def find_recent(self, limit: int = 10) -> List[AuthLog]:
        return await AuthLog.find_all().sort("-created_at").limit(limit).to_list()
