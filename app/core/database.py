from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models.auth_log import AuthLog
from app.models.payment_history import PaymentHistory

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(lambda _: None)


async def init_mongo():
    client = AsyncIOMotorClient(settings.MONGO_URL)
    db = client[settings.MONGO_DB_NAME]

    await init_beanie(
        database=db,
        document_models=[
            AuthLog,
            PaymentHistory,
        ],
    )
