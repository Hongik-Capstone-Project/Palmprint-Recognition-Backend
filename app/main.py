from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.core import init_db, settings
from app.routers import admin, general


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_db()
    except Exception:
        print("Database initialization skipped.")
    yield
    print("Application shutdown complete.")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "Palmprint Recognition Backend API 문서\n\n"
        "본 문서는 **JWT 인증 기반**으로 구성되어 있으며, "
        "`Authorize` 버튼을 클릭하여 토큰을 입력하면 인증이 필요한 요청도 테스트할 수 있습니다.\n\n"
        "**카테고리별 구성**:\n"
        "- 일반 사용자 API (`User`, `Auth`, `Device` 등)\n"
        "- 관리자 전용 API (`Admin-*` 그룹)\n"
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


app.include_router(general.auth_router.router)
app.include_router(general.user_router.router)
app.include_router(general.institution_router.router)
app.include_router(general.payment_router.router)
app.include_router(general.palmprint_router.router)
app.include_router(general.verification_router.router)
app.include_router(general.device_router.router)

app.include_router(admin.admin_user_router.router)
app.include_router(admin.admin_palmprint_router.router)
app.include_router(admin.admin_device_router.router)
app.include_router(admin.admin_report_router.router)
app.include_router(admin.admin_verification_router.router)


@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "ok"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT 토큰을 입력하세요. 예: `Bearer eyJhbGciOi...`",
        }
    }

    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
