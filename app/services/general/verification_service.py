from beanie import PydanticObjectId
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.models.report import Report
from app.repositories.auth_log_repository import AuthLogRepository
from app.repositories.report_repository import ReportRepository


class VerificationService:
    def __init__(
        self,
        session: Session,
        auth_log_repo: AuthLogRepository,
        report_repo: ReportRepository,
    ):
        self.session = session
        self.auth_log_repo = auth_log_repo
        self.report_repo = report_repo

    async def get_verifications(self, payload: dict):
        result = await self.auth_log_repo.find_by_user(payload["user"]["id"])
        result.sort(key=lambda x: x.created_at, reverse=True)
        return result

    async def report_verification(self, payload: dict, log_id: str, reason: str):
        try:
            oid = PydanticObjectId(log_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid log_id",
            )

        auth_log = await self.auth_log_repo.get_by_id(oid)
        if not auth_log:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Auth log not found"
            )
        if auth_log.user_id != payload["user"]["id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
            )

        exists = await self.session.execute(
            self.report_repo.get_by_auth_log_query(str(oid))
        )
        if exists.scalar_one_or_none() is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Already reported"
            )

        report = Report(
            user_id=payload["user"]["id"],
            auth_log_id=str(oid),
            description=reason,
        )

        try:
            self.session.add(report)
            await self.session.commit()
            await self.session.refresh(report)
            return report
        except Exception:
            await self.session.rollback()
            raise
