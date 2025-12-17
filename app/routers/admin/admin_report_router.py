from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.core import _require_admin, get_db
from app.repositories.report_repository import ReportRepository
from app.schemas.report import ReportResponse
from app.services.admin.admin_report_service import AdminReportService

router = APIRouter(
    prefix="/api/admin/reports",
    tags=["Admin-Reports"],
    dependencies=[Depends(_require_admin)],
)


def get_admin_report_service(
    session: Session = Depends(get_db),
    report_repo: ReportRepository = Depends(ReportRepository),
):
    return AdminReportService(session, report_repo)


@router.get("", response_model=Page[ReportResponse], status_code=status.HTTP_200_OK)
async def get_reports(
    params: Params = Depends(),
    service: AdminReportService = Depends(get_admin_report_service),
):
    query = service.get_reports_query()
    return await paginate(service.session, query)


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
