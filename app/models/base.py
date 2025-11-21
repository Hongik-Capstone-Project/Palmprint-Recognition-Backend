# app/models/base.py

from datetime import datetime

from sqlalchemy import BigInteger, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


#
# 모든 엔티티가 상속받을 기본 클래스
class Base(DeclarativeBase):
    """
    SQLAlchemy DeclarativeBase를 상속받아 모든 모델이 사용할 공통 속성을 정의합니다.
    """

    # 💡 모든 테이블에 공통으로 필요한 컬럼 정의

    # Primary Key (PK) 컬럼: 모든 테이블의 PK는 'id'로 BigInteger 타입을 사용합니다.
    # auto-increment를 위해 mapped_column에서 primary_key=True를 설정합니다.
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)

    # 생성 시각 컬럼: func.now()를 사용해 레코드가 생성될 때 서버 시각을 기록합니다.
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())


# 💡 참고: Mapped[int]를 사용해도 Python에서 처리 가능하지만,
# ERD에서 BigINT를 명시했으므로 DB 타입 BigInteger를 명시적으로 사용했습니다.
