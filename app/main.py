from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.database import init_db
from app.routers.general import (
    auth_router,
    device_router,
    institution_router,
    palmprint_router,
    payment_router,
    user_router,
    verification_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    print("Application shutdown complete.")


app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION, lifespan=lifespan)

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(institution_router.router)
app.include_router(payment_router.router)
app.include_router(palmprint_router.router)
app.include_router(verification_router.router)
app.include_router(device_router.router)


@app.get("/")
def health_check():
    return {"status": "ok"}
