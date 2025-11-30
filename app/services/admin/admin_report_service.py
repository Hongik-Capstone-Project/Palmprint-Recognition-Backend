from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.repositories.report_repository import ReportRepository


class AdminReportService:
    def __init__(self, session: Session, report_repo: ReportRepository):
        self.session = session
        self.report_repo = report_repo

    async def get_reports(self):
        query = self.report_repo.get_query()
        result = await self.session.execute(query)
        return result.scalars().unique().all()

    async def get_report_detail(self, report_id: int):
        query = self.report_repo.get_by_id_query(report_id)
        result = await self.session.execute(query)
        report = result.scalar_one_or_none()
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        return report

    async def update_report_status(self, report_id: int, status_str: str):
        query = self.report_repo.get_by_id_query(report_id)
        result = await self.session.execute(query)
        report = result.scalar_one_or_none()
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")

        report.status = status_str  # ORM 모델 필드 직접 수정.
        await self.session.commit()
        await self.session.refresh(report)
        return report

    async def delete_report(self, report_id: int):
        query = self.report_repo.get_by_id_query(report_id)
        result = await self.session.execute(query)
        report = result.scalar_one_or_none()
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")

        await self.session.delete(report)
        await self.session.commit()
