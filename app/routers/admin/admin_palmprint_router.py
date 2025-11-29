from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.repositories.user_repository import UserRepository
from app.services.admin.admin_palmprint_service import AdminPalmprintService

router = APIRouter(prefix="/api/admin/palmprints", tags=["Admin-Palmprints"])


async def get_db_session():
    # 실제 세션 yield logic
    pass


def get_admin_palmprint_service(
    session: Session = Depends(get_db_session),
    user_repo: UserRepository = Depends(UserRepository),
):
    return AdminPalmprintService(session, user_repo)


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_palmprints(
    service: AdminPalmprintService = Depends(get_admin_palmprint_service),
):
    return await service.get_all_palmprints()


@router.post("/{user_id}", status_code=status.HTTP_201_CREATED)
async def register_user_palmprint(user_id: int):
    # DTO를 받아 서비스 호출 로직 필요
    return {"message": f"Palmprint registered for user {user_id}"}


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_palmprint(
    user_id: int, service: AdminPalmprintService = Depends(get_admin_palmprint_service)
):
    await service.delete_user_palmprint(user_id)
    return None
