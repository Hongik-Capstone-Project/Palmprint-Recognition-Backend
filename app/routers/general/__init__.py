from . import (
    auth_router,
    device_router,
    payment_router,
    user_institution_router,
    user_palm_router,
    user_router,
    verification_router,
)

__all__ = [
    "auth_router",
    "user_router",
    "user_institution_router",
    "payment_router",
    "user_palm_router",
    "verification_router",
    "device_router",
]
