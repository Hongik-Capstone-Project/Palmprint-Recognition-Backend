from beanie import PydanticObjectId
from fastapi import HTTPException

from app.repositories.auth_log_repository import AuthLogRepository
from app.schemas.auth_log import VerificationSummaryResponse


class AdminVerificationService:
    def __init__(self, auth_log_repo: AuthLogRepository):
        self.auth_log_repo = auth_log_repo

    async def get_all_verifications(self):
        return await self.auth_log_repo.find_all()

    async def get_verification_detail(self, verification_id: PydanticObjectId):
        log = await self.auth_log_repo.get_by_id(verification_id)
        if not log:
            raise HTTPException(status_code=404, detail="Verification log not found")
        return log

    async def get_summary(self):
        total_verifications = await self.auth_log_repo.count_all()
        success_count = await self.auth_log_repo.count_success(True)

        total_users = await self.auth_log_repo.count_distinct_users()

        registered_palms = 0

        success_rate = 0.0
        if total_verifications > 0:
            success_rate = round((success_count / total_verifications) * 100, 1)

        return VerificationSummaryResponse(
            total_users=total_users,
            registered_palms=registered_palms,
            total_verifications=total_verifications,
            success_rate=success_rate,
        )
