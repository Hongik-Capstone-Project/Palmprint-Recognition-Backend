# app/models/__init__.py

# 모든 엔티티 파일에서 핵심 클래스들을 import
from .base import Base
from .user import User
from .institution import Institution
from .role import Role
from .payment_method import PaymentMethod
from .device import Device
from .report import Report
from .payment_history import PaymentHistory
from .auth_log import AuthLog
from .user_institution import UserInstitution
from .user_institution_role import UserInstitutionRole

# 외부에서 'from app.models import *'를 사용할 때 노출할 클래스 지정
__all__ = [
    "Base",
    "User",
    "Institution",
    "Role",
    "PaymentMethod",
    "Device",
    "Report",
    "PaymentHistory",
    "AuthLog",
    "UserInstitution",
    "UserInstitutionRole",
]