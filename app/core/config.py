from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # 1. 기본 프로젝트 설정
    PROJECT_NAME: str = "Palmprint Recognition Backend"
    VERSION: str = "0.1.0"

    # 2. .env에서 읽어올 변수들 (여기에 선언해야 값을 채워줌)
    # 값을 비워두면 .env에 없을 때 에러를 내서 실수를 방지
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    # 3. 설정 관리 (Pydantic V2 최신 문법)
    # .env 파일을 읽으라고 명시하는 부분
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # <--- 모르는 변수는 에러 내지 말고 무시
    )

    # 4. 흩어진 정보들을 모아서 'DB 접속 주소'를 자동으로 만드는 함수
    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        return f"mysql+asyncmy://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


# 설정 인스턴스 생성
settings = Settings()
