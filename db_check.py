import os
import sys

# 현재 위치를 모듈 검색 경로에 추가 (app 폴더를 찾기 위해)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text

from app.core.config import settings


def test_connection():
    print("🔄 데이터베이스 연결을 시도하는 중...")

    try:
        # 1. 설정에서 주소 가져오기
        db_url = settings.SQLALCHEMY_DATABASE_URL

        # 2. 엔진 생성 (연결 도구)
        engine = create_engine(db_url)

        # 3. 실제 연결 시도
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("\n✅ [성공] 데이터베이스 연결에 성공했습니다!")
            print(f"🔗 연결된 DB: {settings.DB_NAME}")
            print(f"🛠  접속 계정: {settings.DB_USER}")

    except Exception as e:
        print("\n❌ [실패] 연결할 수 없습니다.")
        print("--------------------------------------------------")
        print(f"에러 내용: {e}")
        print("--------------------------------------------------")
        print(
            "💡 팁: 비밀번호, 포트, DB 이름이 정확한지 .env 파일을 다시 확인해보세요."
        )


if __name__ == "__main__":
    test_connection()
