from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload

from app.models.user_palm import UserPalm

from .base import BaseRepository


class UserPalmRepository(BaseRepository[UserPalm]):
    """손바닥 임베딩 데이터 접근 레포지토리"""

    def __init__(self):
        super().__init__(UserPalm)

    def _with_relationships(self, stmt):
        """User 관계 포함"""
        return stmt.options(selectinload(UserPalm.user))

    def get_query(self):
        """전체 조회 쿼리"""
        return self._with_relationships(select(UserPalm))

    def get_by_id_query(self, id: int):
        """ID로 단건 조회 쿼리"""
        return self._with_relationships(select(UserPalm).where(UserPalm.id == id))

    def get_by_user_id_query(self, user_id: int):
        """특정 유저의 모든 손바닥 임베딩 조회 쿼리"""
        return self._with_relationships(
            select(UserPalm).where(UserPalm.user_id == user_id)
        )

    def get_all_embeddings_query(self):
        """전체 임베딩 리스트 조회 쿼리 (인증용)

        인증 시 모든 등록된 임베딩과 비교하기 위해 사용
        관계 로딩 없이 필요한 컬럼만 조회
        """
        return select(UserPalm.id, UserPalm.user_id, UserPalm.embedding)

    def delete_by_id_query(self, id: int):
        """ID로 삭제 쿼리"""
        return delete(UserPalm).where(UserPalm.id == id)

    def delete_by_user_id_query(self, user_id: int):
        """특정 유저의 모든 손바닥 데이터 삭제 쿼리"""
        return delete(UserPalm).where(UserPalm.user_id == user_id)
