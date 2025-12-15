from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserCreateResponse


class UserService:
    def __init__(self, session: Session, user_repo: UserRepository):
        self.session = session
        self.user_repo = user_repo

    async def create_user(self, data: UserCreate) -> UserCreateResponse:
        query = self.user_repo.get_by_email_query(str(data.email))
        result = await self.session.execute(query)
        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists",
            )

        user = User(
            email=str(data.email),
            password=hash_password(data.password),
            name=data.name,
            phone_number=data.phone_number,
        )
        self.session.add(user)

        try:
            await self.session.flush()
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists",
            )
        except Exception:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Server error occurred",
            )

        await self.session.refresh(user)

        return user

    async def get_user(self, user_id: int):
        pass

    async def get_me(self, user_id: int):
        pass

    async def delete_user(self, user_id: int):
        pass
