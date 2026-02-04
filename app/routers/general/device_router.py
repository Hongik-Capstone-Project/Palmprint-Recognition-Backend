from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.core import get_db
from app.repositories.device_repository import DeviceRepository
from app.repositories.payment_method_repository import PaymentMethodRepository
from app.repositories.user_institution_repository import UserInstitutionRepository
from app.repositories.user_institution_role_repository import (
    UserInstitutionRoleRepository,
)
from app.repositories.user_palm_repository import UserPalmRepository
from app.repositories.user_repository import UserRepository
from app.schemas.device import DeviceVerificationRequest, DeviceVerificationResponse
from app.services.admin.admin_user_service import AdminUserService
from app.services.general.device_service import DeviceService
from app.services.general.payment_service import PaymentService
from app.services.general.user_institution_service import UserInstitutionService
from app.services.general.user_palm_service import UserPalmService

router = APIRouter(
    prefix="/api/devices",
    tags=["Devices"],
)


async def get_device_service(
    session: Session = Depends(get_db),
    device_repo: DeviceRepository = Depends(DeviceRepository),
    user_repo: UserRepository = Depends(UserRepository),
    payment_method_repo: PaymentMethodRepository = Depends(PaymentMethodRepository),
    user_palm_repo: UserPalmRepository = Depends(UserPalmRepository),
    user_institution_repo: UserInstitutionRepository = Depends(
        UserInstitutionRepository
    ),
    user_role_repo: UserInstitutionRoleRepository = Depends(
        UserInstitutionRoleRepository
    ),
):
    admin_user_service = AdminUserService(
        session, user_repo, user_institution_repo, user_role_repo
    )
    user_institution_service = UserInstitutionService(session, user_institution_repo)
    payment_service = PaymentService(session, payment_method_repo)
    user_palm_service = UserPalmService(session, user_palm_repo)

    return DeviceService(
        session=session,
        device_repo=device_repo,
        admin_user_service=admin_user_service,
        user_institution_service=user_institution_service,
        payment_service=payment_service,
        user_palm_service=user_palm_service,
    )


@router.post(
    "/verificate",
    response_model=DeviceVerificationResponse,
    status_code=status.HTTP_200_OK,
)
async def verificate_palmprint(
    data: DeviceVerificationRequest,
    service: DeviceService = Depends(get_device_service),
):
    try:
        return await service.verify_palmprint(data)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
