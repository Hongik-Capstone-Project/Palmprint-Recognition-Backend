from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.repositories import AuthLogRepository  # 가상의 레포지토리
from app.schemas.auth_log import AuthLogResponse
from app.services.admin.admin_verification_service import AdminVerificationService

router = APIRouter(prefix="/api/admin/verifications", tags=["Admin-Verifications"])


async def get_db_session():
    # 실제 세션 yield 로직
    pass


def get_admin_verification_service(
    session: Session = Depends(get_db_session),
    auth_log_repo: AuthLogRepository = Depends(AuthLogRepository),
):
    return AdminVerificationService(session, auth_log_repo)


@router.get("", response_model=list[AuthLogResponse], status_code=status.HTTP_200_OK)
async def get_all_verifications(
    service: AdminVerificationService = Depends(get_admin_verification_service),
):
    return await service.get_all_verifications()


@router.get(
    "/{verification_id}", response_model=AuthLogResponse, status_code=status.HTTP_200_OK
)
async def get_verification_detail(
    verification_id: int,
    service: AdminVerificationService = Depends(get_admin_verification_service),
):
    return await service.get_verification_detail(verification_id)
