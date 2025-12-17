from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page, Params, paginate

from app.core import _require_admin
from app.repositories.auth_log_repository import AuthLogRepository
from app.schemas.auth_log import AuthLogResponse, VerificationSummaryResponse
from app.services.admin.admin_verification_service import AdminVerificationService

router = APIRouter(
    prefix="/api/admin/verifications",
    tags=["Admin-Verifications"],
    dependencies=[Depends(_require_admin)],
)


def get_admin_verification_service(
    auth_log_repo: AuthLogRepository = Depends(AuthLogRepository),
):
    return AdminVerificationService(auth_log_repo)


@router.get("", response_model=Page[AuthLogResponse])
async def get_all_verifications(
    params: Params = Depends(),
    service: AdminVerificationService = Depends(get_admin_verification_service),
):
    items = await service.get_all_verifications()
    return paginate(items, params)


@router.get(
    "/summary",
    response_model=VerificationSummaryResponse,
    status_code=status.HTTP_200_OK,
)
async def get_verifications_summary(
    service: AdminVerificationService = Depends(get_admin_verification_service),
):
    return await service.get_summary()


@router.get(
    "/{verification_id}",
    response_model=AuthLogResponse,
    status_code=status.HTTP_200_OK,
)
async def get_verification_detail(
    verification_id: PydanticObjectId,
    service: AdminVerificationService = Depends(get_admin_verification_service),
):
    return await service.get_verification_detail(verification_id)
