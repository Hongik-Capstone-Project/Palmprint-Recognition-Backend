from . import (
    auth_router,
    device_router,
    institution_router,
    palmprint_router,
    payment_router,
    user_router,
    verification_router,
)

__all__ = [
    "auth_router",
    "user_router",
    "institution_router",
    "payment_router",
    "palmprint_router",
    "verification_router",
    "device_router",
]
