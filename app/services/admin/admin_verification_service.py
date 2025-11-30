from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession as Session


class AdminVerificationService:
    # def __init__(self, session: Session, auth_log_repo: AuthLogRepository):
    #     self.session = session
    #     self.auth_log_repo = auth_log_repo

    # async def get_all_verifications(self):
    #     query = self.auth_log_repo.get_query()
    #     result = await self.session.execute(query)
    #     return result.scalars().unique().all()

    # async def get_verification_detail(self, verification_id: int):
    #     query = self.auth_log_repo.get_by_id_query(verification_id)
    #     result = await self.session.execute(query)
    #     log = result.scalar_one_or_none()
    #     if not log:
    #         raise HTTPException(status_code=404, detail="Verification log not found")
    #     return log

    # async def delete_verification(self, verification_id: int):
    #     query = self.auth_log_repo.get_by_id_query(verification_id)
    #     result = await self.session.execute(query)
    #     log = result.scalar_one_or_none()
    #     if not log:
    #         raise HTTPException(status_code=404, detail="Verification log not found")

    #     await self.session.delete(log)
    #     await self.session.commit()
    pass
