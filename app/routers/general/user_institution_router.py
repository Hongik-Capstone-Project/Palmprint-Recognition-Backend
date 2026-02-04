from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.core import _get_current_payload
from app.core.database import get_db
from app.repositories.user_institution_repository import UserInstitutionRepository
from app.schemas.user_institution import UserInstitutionCreate, UserInstitutionResponse
from app.services.general import UserInstitutionService

router = APIRouter(prefix="/api/users/me/institutions", tags=["User-Institutions"])


def get_user_institution_service(
    session: Session = Depends(get_db),
) -> UserInstitutionService:
    return UserInstitutionService(
        session=session,
        user_institution_repo=UserInstitutionRepository(),
    )


@router.get(
    "", status_code=status.HTTP_200_OK, response_model=list[UserInstitutionResponse]
)
async def get_institutions(
    payload: dict = Depends(_get_current_payload),
    service: UserInstitutionService = Depends(get_user_institution_service),
):
    return await service.get_institutions(payload["user"]["id"])


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=UserInstitutionResponse
)
async def add_institution(
    body: UserInstitutionCreate,
    payload: dict = Depends(_get_current_payload),
    service: UserInstitutionService = Depends(get_user_institution_service),
):
    return await service.add_institution(payload, body)


@router.delete("/{institution_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_institution(
    institution_id: int,
    payload: dict = Depends(_get_current_payload),
    service: UserInstitutionService = Depends(get_user_institution_service),
):
    await service.delete_institution(payload, institution_id)
    return None
