from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.core import _require_admin, get_db
from app.repositories.user_institution_repository import UserInstitutionRepository
from app.repositories.user_institution_role_repository import (
    UserInstitutionRoleRepository,
)
from app.repositories.user_repository import UserRepository
from app.schemas.user import (
    UserAdminCreate,
    UserCreateResponse,
    UserResponse,
    UserUpdate,
)
from app.schemas.user_institution_role import (
    UserInstitutionRoleCreate,
    UserInstitutionRoleResponse,
)
from app.services.admin.admin_user_service import AdminUserService

router = APIRouter(
    prefix="/api/admin/users",
    tags=["Admin-Users"],
    dependencies=[Depends(_require_admin)],
)


def get_admin_user_service(
    session: Session = Depends(get_db),
    user_repo: UserRepository = Depends(UserRepository),
    user_institution_repo: UserInstitutionRepository = Depends(
        UserInstitutionRepository
    ),
    user_role_repo: UserInstitutionRoleRepository = Depends(
        UserInstitutionRoleRepository
    ),
):
    return AdminUserService(session, user_repo, user_institution_repo, user_role_repo)


@router.get("", response_model=Page[UserResponse], status_code=status.HTTP_200_OK)
async def get_users(
    params: Params = Depends(),
    service: AdminUserService = Depends(get_admin_user_service),
):
    query = service.get_users_query()
    return await paginate(service.session, query)


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_detail(
    user_id: int, service: AdminUserService = Depends(get_admin_user_service)
):
    return await service.get_user_detail(user_id)


@router.post("", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    data: UserAdminCreate, service: AdminUserService = Depends(get_admin_user_service)
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
