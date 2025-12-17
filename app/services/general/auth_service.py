import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenResponse


def build_user_claims(user: User) -> dict:
    payment_methods = []
    for pm in user.payment_methods or []:
        if hasattr(pm, "id"):
            payment_methods.append(pm.id)

    user_institutions = []
    for ui in user.user_institutions or []:
        user_institutions.append(
            {
                "institution_id": ui.institution_id,
                "local_id": ui.local_id,
                "student_id": ui.student_id,
            }
        )

    user_institution_roles = []
    for uir in user.user_institution_roles or []:
        user_institution_roles.append(
            {
                "role_id": uir.role_id,
                "institution_id": uir.institution_id,
            }
        )

    return {
        "user": {
            "id": str(user.id),
            "email": user.email,
            "name": user.name,
            "phone_number": user.phone_number,
            "payment_methods": payment_methods,
            "user_institutions": user_institutions,
            "user_institution_roles": user_institution_roles,
        }
    }


class AuthService:
    def __init__(self, session: Session, user_repo: UserRepository):
        self.session = session
        self.user_repo = user_repo

    async def login(self, email: str, password: str) -> TokenResponse:
        query = self.user_repo.get_by_email_query(email)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()

        if (user is None) or (not verify_password(password, user.password)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        access_expires = 3600
        refresh_expires = 30 * 24 * 3600

        claims = build_user_claims(user)
        jti = uuid.uuid4().hex

        access_token = create_access_token(
            data={"sub": str(user.id), "jti": jti, **claims},
            expires_delta=access_expires,
        )
        refresh_token = create_refresh_token(
            data={"sub": str(user.id), "jti": jti},
            expires_delta=refresh_expires,
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=access_expires,
            refresh_expires_in=refresh_expires,
        )

    async def refresh(self, refresh_token: str) -> TokenResponse:
        payload = decode_token(refresh_token)
        if (not payload) or (payload.get("type") != "refresh"):
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        sub = payload.get("sub")
        if not sub:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        try:
            user_id = int(sub)
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        query = self.user_repo.get_by_id_query(user_id)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        access_expires = 3600
        jti = payload.get("jti") or uuid.uuid4().hex
        claims = build_user_claims(user)

        access_token = create_access_token(
            data={"sub": str(user.id), "jti": jti, **claims},
            expires_delta=access_expires,
        )

        refresh_expires_in = None
        exp = payload.get("exp")
        if exp:
            now_ts = int(datetime.now(timezone.utc).timestamp())
            refresh_expires_in = max(0, int(exp) - now_ts)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=access_expires,
            refresh_expires_in=refresh_expires_in,
        )
