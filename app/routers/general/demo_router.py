from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.core import get_db
from app.repositories.user_palm_repository import UserPalmRepository
from app.schemas.demo import (
    DemoRegisterRequest,
    DemoRegisterResponse,
    DemoVerifyRequest,
    DemoVerifyResponse,
)
from app.services.general.demo_service import DemoService
from app.services.general.user_palm_service import UserPalmService

router = APIRouter(prefix="/api/demo", tags=["Demo"])


def get_demo_service(
    session: Session = Depends(get_db),
    user_palm_repo: UserPalmRepository = Depends(UserPalmRepository),
):
    user_palm_service = UserPalmService(session, user_palm_repo)
    return DemoService(session, user_palm_service)


@router.post(
    "/register",
    response_model=DemoRegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def demo_register(
    data: DemoRegisterRequest,
    service: DemoService = Depends(get_demo_service),
):
    """데모용 장문 등록 (인증 불필요)"""
    return await service.register(data)


@router.post(
    "/verify",
    response_model=DemoVerifyResponse,
    status_code=status.HTTP_200_OK,
)
async def demo_verify(
    data: DemoVerifyRequest,
    service: DemoService = Depends(get_demo_service),
):
    """데모용 장문 검증 (인증 불필요)"""
    return await service.verify(data.palmprint_data)
