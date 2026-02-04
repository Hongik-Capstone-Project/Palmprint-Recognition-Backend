from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.core import _get_current_payload, get_db
from app.repositories.user_palm_repository import UserPalmRepository
from app.schemas.user_palm import (
    UserPalmListResponse,
    UserPalmRegister,
    UserPalmRegisterResponse,
    UserPalmResponse,
)
from app.services.general.user_palm_service import UserPalmService

router = APIRouter(prefix="/api/users/me/palmprints", tags=["User Palms"])


def get_user_palm_service(
    session: Session = Depends(get_db),
    user_palm_repo: UserPalmRepository = Depends(UserPalmRepository),
):
    """UserPalmService 의존성 주입"""
    return UserPalmService(session, user_palm_repo)


@router.post(
    "",
    response_model=UserPalmRegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_palm(
    data: UserPalmRegister,
    payload=Depends(_get_current_payload),
    service: UserPalmService = Depends(get_user_palm_service),
):
    user_palm = await service.register_palm(payload.get("user").get("id"), data)

    return UserPalmRegisterResponse(
        id=user_palm.id,
        user_id=user_palm.user_id,
        created_at=user_palm.created_at,
        message="Palm registered successfully",
    )


@router.get(
    "",
    response_model=UserPalmListResponse,
    status_code=status.HTTP_200_OK,
)
async def get_my_palms(
    payload=Depends(_get_current_payload),
    service: UserPalmService = Depends(get_user_palm_service),
):
    palms = await service.get_user_palms(payload.get("user").get("id"))

    return UserPalmListResponse(
        palms=[
            UserPalmResponse(
                id=palm.id,
                user_id=palm.user_id,
                created_at=palm.created_at,
                updated_at=palm.updated_at,
            )
            for palm in palms
        ],
        total_count=len(palms),
    )


@router.delete(
    "/me/all",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_all_my_palms(
    payload=Depends(_get_current_payload),
    service: UserPalmService = Depends(get_user_palm_service),
):
    user_block = payload.get("user") if payload else None
    user_id = user_block.get("id") if user_block else None

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    await service.delete_all_user_palms(user_id)
    return None


@router.delete(
    "/me/{palm_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_palm(
    palm_id: int,
    payload=Depends(_get_current_payload),
    service: UserPalmService = Depends(get_user_palm_service),
):
    user_block = payload.get("user") if payload else None
    user_id = user_block.get("id") if user_block else None

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    await service.delete_palm(palm_id, user_id)
    return None
