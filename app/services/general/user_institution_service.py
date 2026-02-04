from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.models.user_institution import UserInstitution
from app.repositories.user_institution_repository import UserInstitutionRepository
from app.schemas.user_institution import UserInstitutionCreate


class UserInstitutionService:
    def __init__(
        self, session: Session, user_institution_repo: UserInstitutionRepository
    ):
        self.session = session
        self.user_institution_repo = user_institution_repo

    async def get_institutions(self, user_id: int):
        result = await self.session.execute(
            self.user_institution_repo.get_by_user_query(user_id)
        )
        return result.scalars().all()

    async def get_institution(
        self,
        user_id: int,
        institution_id: int,
    ):
        result = await self.session.execute(
            self.user_institution_repo.get_by_user_and_institution_query(
                user_id, institution_id
            )
        )
        user_institution = result.scalar_one_or_none()
        if not user_institution:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
            )
        return user_institution

    async def add_institution(
        self, payload: dict, institution_data: UserInstitutionCreate
    ):
        institution_id = institution_data.institution_id
        institution_user_id = institution_data.institution_user_id

        result = await self.session.execute(
            self.user_institution_repo.get_by_user_and_institution_query(
                payload["user"]["id"], institution_id
            )
        )
        if result.scalar_one_or_none() is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Already added"
            )

        user_institution = UserInstitution(
            user_id=payload["user"]["id"],
            institution_id=institution_id,
            institution_user_id=institution_user_id,
        )

        try:
            self.session.add(user_institution)
            await self.session.commit()
            result = await self.session.execute(
                self.user_institution_repo.get_by_user_and_institution_query(
                    payload["user"]["id"], institution_id
                )
            )
            return result.scalar_one()
        except Exception:
            await self.session.rollback()
            raise

    async def delete_institution(self, payload: dict, institution_id: int):
        result = await self.session.execute(
            self.user_institution_repo.get_by_user_and_institution_query(
                payload["user"]["id"], institution_id
            )
        )
        user_institution = result.scalar_one_or_none()
        if not user_institution:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
            )

        try:
            await self.session.delete(user_institution)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
