from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession as Session  # DB 세션 타입 가정

from app.models.user import User  # ORM Model import (관계 로딩을 위해 필요)
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
        session: Session,  # 세션 주입
        user_repo: UserRepository,
        user_role_repo: UserInstitutionRoleRepository,
    ):
        self.session = session
        self.user_repo = user_repo
        self.user_role_repo = user_role_repo

    async def get_users(self):
        # 쿼리 생성 후 세션으로 실행
        # relationships 로드를 위해 options(selectinload(User.relationships)) 추가 필요.
        query = self.user_repo.get_query()
        result = await self.session.execute(query)
        return result.scalars().unique().all()

    async def get_user_detail(self, user_id: int):
        # ID 쿼리 생성
        query = self.user_repo.get_by_id_query(user_id)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def register_user(self, user_data: UserCreate):
        # CREATE 로직: Session에 새 객체를 추가하고 커밋
        user_dict = user_data.model_dump()
        user_dict["password"] = f"hashed_{user_dict['password']}"
        new_user_model = User(**user_dict)
        self.session.add(new_user_model)
        await self.session.commit()
        await self.session.refresh(new_user_model)
        return new_user_model

    async def update_user(self, user_id: int, user_data: UserUpdate):
        # UPDATE 로직: 쿼리로 객체를 찾고 수정 후 커밋
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
        # DELETE 로직
        query = self.user_repo.get_by_id_query(user_id)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        await self.session.delete(user)
        await self.session.commit()
        return {"message": "User deleted successfully"}

    async def grant_user_role(self, user_id: int, role_data: UserInstitutionRoleCreate):
        if role_data.user_id != user_id:
            raise HTTPException(status_code=400, detail="User ID mismatch")

        # UserInstitutionRole 모델 생성 및 커밋
        new_role_model = self.user_role_repo.model(
            **role_data.model_dump()
        )  # model 속성은 BaseRepository에 있음
        self.session.add(new_role_model)
        await self.session.commit()
        await self.session.refresh(new_role_model)
        return new_role_model
