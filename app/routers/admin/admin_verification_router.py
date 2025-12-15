from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.core import get_db, require_admin
from app.schemas.auth_log import AuthLogResponse
from app.services.admin.admin_verification_service import AdminVerificationService

router = APIRouter(
    prefix="/api/admin/verifications",
    tags=["Admin-Verifications"],
    dependencies=[Depends(require_admin)],
)


# def get_admin_verification_service(
#     session: Session = Depends(get_db()),
#     auth_log_repo: AuthLogRepository = Depends(AuthLogRepository),
# ):
#     return AdminVerificationService(session, auth_log_repo)


# @router.get("", response_model=list[AuthLogResponse], status_code=status.HTTP_200_OK)
# async def get_all_verifications(
#     service: AdminVerificationService = Depends(get_admin_verification_service),
# ):
#     return await service.get_all_verifications()


# @router.get(
#     "/{verification_id}", response_model=AuthLogResponse, status_code=status.HTTP_200_OK
# )
# async def get_verification_detail(
#     verification_id: int,
#     service: AdminVerificationService = Depends(get_admin_verification_service),
# ):
#     return await service.get_verification_detail(verification_id)
