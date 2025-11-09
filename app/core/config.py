from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Palmprint Recognition Backend"
    VERSION: str = "0.1.0"
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"


settings = Settings()
