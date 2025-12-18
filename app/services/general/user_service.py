from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, session: Session, user_repo: UserRepository):
        self.session = session
        self.user_repo = user_repo

    async def create_user(self, data: UserCreate):
        query = self.user_repo.get_by_email_query(str(data.email))
        result = await self.session.execute(query)
        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists",
            )

        user = User(
            email=str(data.email), password=hash_password(data.password), name=data.name
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

    async def delete_me(self, payload):
        user_block = payload.get("user") if payload else None
        user_id = user_block.get("id") if user_block else None

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )

        query = self.user_repo.get_by_id_query(user_id)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        try:
            await self.session.execute(self.user_repo.delete_by_id_query(user_id))
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Server error occurred",
            )
