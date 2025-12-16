# app/models/base.py

from datetime import datetime

from sqlalchemy import BigInteger, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# 모든 엔티티가 상속받을 기본 클래스


# 1. 기본 선언적 베이스 클래스
class Base(DeclarativeBase):
    pass


# 2. 생성 시간 Mixin (모든 모델이 씀)
class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())


# 3. 정수형 ID Mixin (User, Report 등 대부분의 모델이 씀)
class IntPKMixin:
    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, index=True, autoincrement=True
    )
