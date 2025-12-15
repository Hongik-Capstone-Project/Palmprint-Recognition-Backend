from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.core import get_current_payload, get_db
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, RefreshRequest, TokenResponse
from app.services.general.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["Auth"])


def get_auth_service(
    session: Session = Depends(get_db),
    user_repo: UserRepository = Depends(UserRepository),
):
    return AuthService(session, user_repo)


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(data: LoginRequest, service: AuthService = Depends(get_auth_service)):
    return await service.login(str(data.email), data.password)


@router.post("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def refresh(
    data: RefreshRequest, service: AuthService = Depends(get_auth_service)
):
    return await service.refresh(data.refresh_token)
