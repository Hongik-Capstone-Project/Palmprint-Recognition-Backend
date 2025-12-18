from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page, Params, paginate
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.core import _get_current_payload
from app.core.database import get_db
from app.repositories.auth_log_repository import AuthLogRepository
from app.repositories.report_repository import ReportRepository
from app.schemas.auth_log import AuthLogResponse, VerificationReportCreate
from app.services.general.verification_service import VerificationService

router = APIRouter(
    prefix="/api/users/me/verifications",
    tags=["Verifications"],
    dependencies=[Depends(_get_current_payload)],
)


def get_verification_service(session: Session = Depends(get_db)) -> VerificationService:
    return VerificationService(
        session=session,
        auth_log_repo=AuthLogRepository(),
        report_repo=ReportRepository(),
    )


@router.get("", status_code=status.HTTP_200_OK, response_model=Page[AuthLogResponse])
async def get_verifications(
    params: Params = Depends(),
    payload: dict = Depends(_get_current_payload),
    service: VerificationService = Depends(get_verification_service),
):
    items = await service.get_verifications(payload)
    return paginate(items, params)


@router.post("/{log_id}/report", status_code=status.HTTP_201_CREATED)
async def report_verification(
    log_id: str,
    body: VerificationReportCreate,
    payload: dict = Depends(_get_current_payload),
    service: VerificationService = Depends(get_verification_service),
):
    return await service.report_verification(payload, log_id, body.reason)
