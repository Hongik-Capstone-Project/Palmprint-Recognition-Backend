import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_palm_repository import UserPalmRepository
from app.schemas.demo import DemoRegisterRequest, DemoRegisterResponse, DemoVerifyResponse
from app.services.general.user_palm_service import UserPalmService
from app.schemas.user_palm import UserPalmRegister
from app.utils.base64_image import extract_base64_image


class DemoService:

    def __init__(self, session: Session, user_palm_service: UserPalmService):
        self.session = session
        self.user_palm_service = user_palm_service

    @staticmethod
    def mask_name(name: str) -> str:
        """이름의 두 번째 문자를 *로 마스킹"""
        if len(name) <= 1:
            return name
        return name[0] + "*" + name[2:]

    async def register(self, data: DemoRegisterRequest) -> DemoRegisterResponse:
        # 1. 더미 유저 생성
        dummy_email = f"demo_{uuid.uuid4().hex[:8]}@demo.local"
        dummy_password = hash_password(uuid.uuid4().hex)

        user = User(
            email=dummy_email,
            password=dummy_password,
            name=data.name,
        )
        self.session.add(user)

        try:
            await self.session.flush()
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create demo user: {str(e)}",
            )

        # 2. 장문 등록 (기존 서비스 재사용)
        palm = await self.user_palm_service.register_palm(
            user.id, UserPalmRegister(palmprint_data=data.palmprint_data)
        )

        return DemoRegisterResponse(
            id=palm.id,
            user_id=user.id,
            palm_id=palm.id,
            name=data.name,
            created_at=palm.created_at,
        )

    async def verify(self, palmprint_data: str) -> DemoVerifyResponse:
        # 1. 임베딩 추출
        embedding = await self.user_palm_service.get_embedding_from_image(
            extract_base64_image(palmprint_data)
        )

        # 2. 매칭
        match_result = await self.user_palm_service.find_matching_user(embedding)

        if not match_result.matched:
            return DemoVerifyResponse(
                matched=False,
                similarity_score=match_result.similarity_score,
            )

        # 3. 유저 이름 조회
        from app.repositories.user_repository import UserRepository

        user_repo = UserRepository()
        query = user_repo.get_by_id_query(match_result.user_id)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            return DemoVerifyResponse(matched=False)

        return DemoVerifyResponse(
            matched=True,
            name=self.mask_name(user.name),
            similarity_score=match_result.similarity_score,
        )
