from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_institution_repository import UserInstitutionRepository
from app.repositories.user_institution_role_repository import (
    UserInstitutionRoleRepository,
)
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.schemas.user_institution_role import UserInstitutionRoleCreate


class AdminUserService:
    def __init__(
        self,
        session: Session,
        user_repo: UserRepository,
        user_institution_repo: UserInstitutionRepository,
        user_role_repo: UserInstitutionRoleRepository,
    ):
        self.session = session
        self.user_repo = user_repo
        self.user_institution_repo = user_institution_repo
        self.user_role_repo = user_role_repo

    def get_users_query(self):
        return select(User)

    async def get_user_detail(self, user_id: int):
        query = self.user_repo.get_by_id_query(user_id)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def register_user(self, user_data: UserCreate):
        query = self.user_repo.get_by_email_query(str(user_data.email))
        result = await self.session.execute(query)
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists",
            )

        new_user_model = User(
            email=str(user_data.email),
            password=hash_password(user_data.password),
            name=user_data.name,
        )
        self.session.add(new_user_model)

        try:
            await self.session.flush()

            if user_data.is_admin == 1 or user_data.is_admin is True:
                institution_id = 1
                role_id = 1

                self.session.add(
                    self.user_institution_repo.model(
                        user_id=new_user_model.id,
                        institution_id=institution_id,
                        institution_user_id="admin",
                    )
                )

                self.session.add(
                    self.user_role_repo.model(
                        user_id=new_user_model.id,
                        institution_id=institution_id,
                        role_id=role_id,
                    )
                )

            await self.session.commit()

        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Conflict occurred",
            )
        except Exception:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Server error occurred",
            )

        await self.session.refresh(new_user_model)
        return new_user_model

    async def update_user(self, user_id: int, user_data: UserUpdate):
        query = self.user_repo.get_by_id_query(user_id)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        update_dict = user_data.model_dump(exclude_unset=True)
        if "password" in update_dict:
            update_dict["password"] = f"hashed_{update_dict['password']}"

        for key, value in update_dict.items():
            setattr(user, key, value)

        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete_user(self, user_id: int):
        query = self.user_repo.get_by_id_query(user_id)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        await self.session.delete(user)
        await self.session.commit()
        return {"message": "User deleted successfully"}

    async def grant_user_role(self, user_id: int, role_data: UserInstitutionRoleCreate):
        new_role_model = self.user_role_repo.model(
            user_id=user_id, **role_data.model_dump()
        )
        self.session.add(new_role_model)
        await self.session.commit()
        await self.session.refresh(new_role_model)
        return new_role_model
