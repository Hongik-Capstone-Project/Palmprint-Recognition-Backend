import math
from typing import Optional

import httpx
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.core.config import settings
from app.models.user_palm import UserPalm
from app.repositories.user_palm_repository import UserPalmRepository
from app.schemas.user_palm import (
    EmbeddingServiceRequest,
    EmbeddingServiceResponse,
    PalmMatchResult,
    UserPalmRegister,
)
from app.utils.base64_image import extract_base64_image


class UserPalmService:

    def __init__(self, session: Session, user_palm_repo: UserPalmRepository):
        self.session = session
        self.user_palm_repo = user_palm_repo

        self.embedding_service_url = settings.EMBEDDING_SERVICE_URL
        self.similarity_threshold = settings.PALM_SIMILARITY_THRESHOLD

    async def get_embedding_from_image(self, base64_image: str) -> list[float]:
        try:
            request_data = EmbeddingServiceRequest(
                base64_image=extract_base64_image(base64_image)
            )

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.embedding_service_url,
                    json=request_data.model_dump(),
                    headers={"Content-Type": "application/json"},
                )
                response.raise_for_status()

                embedding_response = EmbeddingServiceResponse(**response.json())

                return embedding_response.embedding

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid palmprint data: {str(e)}",
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Embedding service unavailable: {str(e)}",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate embedding: {str(e)}",
            )

    @staticmethod
    def calculate_cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
        if len(vec1) != len(vec2):
            raise ValueError(
                f"Vector dimensions must match: {len(vec1)} vs {len(vec2)}"
            )

        # 내적 계산
        dot_product = sum(a * b for a, b in zip(vec1, vec2))

        # 각 벡터의 크기(norm) 계산
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(b * b for b in vec2))

        # 0으로 나누기 방지
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        # 코사인 유사도 = 내적 / (크기1 * 크기2)
        return dot_product / (magnitude1 * magnitude2)

    async def find_matching_user(self, input_embedding: list[float]) -> PalmMatchResult:
        # DB에서 모든 등록된 임베딩 조회 (id, user_id, embedding만)
        query = self.user_palm_repo.get_all_embeddings_query()
        result = await self.session.execute(query)
        registered_palms = result.all()

        if not registered_palms:
            return PalmMatchResult(matched=False)

        # 메모리 상에서 각 임베딩과 코사인 유사도 계산
        best_match: Optional[tuple[int, int, float]] = (
            None  # (palm_id, user_id, similarity)
        )

        for palm_id, user_id, embedding in registered_palms:
            try:
                similarity = self.calculate_cosine_similarity(
                    input_embedding, embedding
                )

                # 가장 높은 유사도 추적
                if best_match is None or similarity > best_match[2]:
                    best_match = (palm_id, user_id, similarity)

            except Exception as e:
                # 특정 임베딩 계산 실패 시 다음으로 진행
                print(f"Error calculating similarity for palm_id={palm_id}: {e}")
                continue

        # 매칭 결과 반환
        if best_match and best_match[2] >= self.similarity_threshold:
            return PalmMatchResult(
                matched=True,
                user_id=best_match[1],
                palm_id=best_match[0],
                similarity_score=best_match[2],
            )
        else:
            return PalmMatchResult(
                matched=False, similarity_score=best_match[2] if best_match else None
            )

    async def register_palm(self, user_id: int, data: UserPalmRegister) -> UserPalm:
        # 1. 임베딩 생성
        embedding = await self.get_embedding_from_image(
            extract_base64_image(data.palmprint_data)
        )

        # 2. DB에 저장
        user_palm = UserPalm(user_id=user_id, embedding=embedding)

        self.session.add(user_palm)

        try:
            await self.session.flush()
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Failed to register palm: {str(e)}",
            )
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Server error occurred: {str(e)}",
            )

        await self.session.refresh(user_palm)
        return user_palm

    async def get_user_palms(self, user_id: int) -> list[UserPalm]:
        query = self.user_palm_repo.get_by_user_id_query(user_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def delete_palm(self, palm_id: int, user_id: int) -> None:
        query = self.user_palm_repo.get_by_id_query(palm_id)
        result = await self.session.execute(query)
        palm = result.scalar_one_or_none()

        if palm is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Palm not found"
            )

        if palm.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this palm",
            )

        try:
            await self.session.execute(self.user_palm_repo.delete_by_id_query(palm_id))
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete palm: {str(e)}",
            )

    async def delete_all_user_palms(self, user_id: int) -> None:
        try:
            await self.session.execute(
                self.user_palm_repo.delete_by_user_id_query(user_id)
            )
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete user palms: {str(e)}",
            )
