from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.models.user import User
from app.repositories.user_repository import UserRepository


class AdminPalmprintService:
    def __init__(self, session: Session, user_repo: UserRepository):
        self.session = session
        self.user_repo = user_repo

    async def get_all_palmprints(self):
        # 모든 사용자 (Palmprint 데이터 존재 여부 확인 쿼리 필요)
        query = self.user_repo.get_query()
        result = await self.session.execute(query)
        # 실제로는 여기서 필요한 필터링 및 DTO 변환 로직이 들어감
        return ["List of filtered palmprint data"]

    async def get_user_palmprint(self, user_id: int):
        query = self.user_repo.get_by_id_query(user_id)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        # user 객체에 palmprint_data라는 가상의 필드가 있다고 가정
        if not hasattr(user, "palmprint_data") or user.palmprint_data is None:
            raise HTTPException(
                status_code=404, detail="Palmprint data not found for user"
            )

        return {"user_id": user_id, "data": "palmprint_detail_placeholder"}

    async def delete_user_palmprint(self, user_id: int):
        query = self.user_repo.get_by_id_query(user_id)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # User 모델의 palmprint_data 필드를 None으로 설정하고 커밋
        if hasattr(user, "palmprint_data"):
            setattr(user, "palmprint_data", None)
            await self.session.commit()

        return {"message": f"Palmprint data for user {user_id} deleted."}
