from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.repositories.report_repository import ReportRepository
from app.schemas.report import ReportResponse
from app.services.admin.admin_report_service import AdminReportService

router = APIRouter(prefix="/api/admin/reports", tags=["Admin-Reports"])


async def get_db_session():
    # 실제 세션 yield 로직
    pass


def get_admin_report_service(
    session: Session = Depends(get_db_session),
    report_repo: ReportRepository = Depends(ReportRepository),
):
    return AdminReportService(session, report_repo)


@router.get("", response_model=list[ReportResponse], status_code=status.HTTP_200_OK)
async def get_reports(service: AdminReportService = Depends(get_admin_report_service)):
    return await service.get_reports()


@router.get(
    "/{report_id}", response_model=ReportResponse, status_code=status.HTTP_200_OK
)
async def get_report_detail(
    report_id: int, service: AdminReportService = Depends(get_admin_report_service)
):
    return await service.get_report_detail(report_id)


@router.patch(
    "/{report_id}/status", response_model=ReportResponse, status_code=status.HTTP_200_OK
)
async def update_report_status(
    report_id: int,
    new_status: str,
    service: AdminReportService = Depends(get_admin_report_service),
):
    return await service.update_report_status(report_id, new_status)
