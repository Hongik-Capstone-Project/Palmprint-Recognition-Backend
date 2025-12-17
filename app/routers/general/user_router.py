from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.core import _get_current_payload, get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserCreateResponse
from app.services.general.user_service import UserService

router = APIRouter(prefix="/api/users", tags=["Users"])


def get_user_service(
    session: Session = Depends(get_db),
    user_repo: UserRepository = Depends(UserRepository),
):
    return UserService(session, user_repo)


@router.post("", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    data: UserCreate,
    service: UserService = Depends(get_user_service),
):
    return await service.create_user(data)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(
    payload=Depends(_get_current_payload),
):
    pass
