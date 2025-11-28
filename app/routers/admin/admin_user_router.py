from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession as Session  # 세션 타입

from app.repositories.user_institution_role_repository import (
    UserInstitutionRoleRepository,
)
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.schemas.user_institution_role import (
    UserInstitutionRoleCreate,
    UserInstitutionRoleResponse,
)
from app.services.admin.admin_user_service import AdminUserService

router = APIRouter(prefix="/api/admin/users", tags=["Admin-Users"])


# 세션 주입을 위한 임시 함수 (실제로는 Dependency Injection 설정 파일에서 제공됨)
async def get_db_session():
    # 실제 DB 세션을 yield 하는 로직이 들어감
    # yield session
    pass


# DI Provider 정의
def get_admin_user_service(
    session: Session = Depends(get_db_session),  # 세션 주입
    user_repo: UserRepository = Depends(UserRepository),
    user_role_repo: UserInstitutionRoleRepository = Depends(
        UserInstitutionRoleRepository
    ),
):
    return AdminUserService(session, user_repo, user_role_repo)


@router.get("", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
async def get_users(service: AdminUserService = Depends(get_admin_user_service)):
    return await service.get_users()


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_detail(
    user_id: int, service: AdminUserService = Depends(get_admin_user_service)
):
    return await service.get_user_detail(user_id)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    data: UserCreate, service: AdminUserService = Depends(get_admin_user_service)
):
    return await service.register_user(data)


@router.patch("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(
    user_id: int,
    data: UserUpdate,
    service: AdminUserService = Depends(get_admin_user_service),
):
    return await service.update_user(user_id, data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int, service: AdminUserService = Depends(get_admin_user_service)
):
    await service.delete_user(user_id)
    return None


@router.post(
    "/{user_id}/role",
    response_model=UserInstitutionRoleResponse,
    status_code=status.HTTP_201_CREATED,
)
async def grant_user_role(
    user_id: int,
    data: UserInstitutionRoleCreate,
    service: AdminUserService = Depends(get_admin_user_service),
):
    return await service.grant_user_role(user_id, data)
