# app/schemas/__init__.py

from .base import BaseSchema
from .device import DeviceCreate, DeviceResponse, DeviceUpdate
from .institution import InstitutionCreate, InstitutionResponse
from .payment_method import (
    PaymentMethodCreate,
    PaymentMethodResponse,
    PaymentMethodUpdate,
)
from .report import ReportCreate, ReportResponse
from .role import RoleCreate, RoleResponse
from .user import UserCreate, UserResponse, UserUpdate

# from .auth_log import AuthLogResponse
# from .payment_history import PaymentHistoryResponse
from .user_institution import UserInstitutionCreate, UserInstitutionResponse
from .user_institution_role import (
    UserInstitutionRoleCreate,
    UserInstitutionRoleResponse,
)

__all__ = [
    "BaseSchema",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "InstitutionCreate",
    "InstitutionResponse",
    "RoleCreate",
    "RoleResponse",
    "PaymentMethodCreate",
    "PaymentMethodUpdate",
    "PaymentMethodResponse",
    "DeviceCreate",
    "DeviceUpdate",
    "DeviceResponse",
    "ReportCreate",
    "ReportResponse",
    # "AuthLogResponse",
    # "PaymentHistoryResponse",
    "UserInstitutionCreate",
    "UserInstitutionResponse",
    "UserInstitutionRoleCreate",
    "UserInstitutionRoleResponse",
]
