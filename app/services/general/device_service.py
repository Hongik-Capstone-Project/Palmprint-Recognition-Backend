from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.models.device import Device
from app.repositories.device_repository import DeviceRepository
from app.schemas.device import DeviceVerificationRequest, DeviceVerificationResponse
from app.schemas.user import UserCreateResponse
from app.services.admin import AdminUserService
from app.services.general.payment_service import PaymentService
from app.services.general.user_institution_service import UserInstitutionService
from app.services.general.user_palm_service import UserPalmService
from app.utils.base64_image import extract_base64_image


class DeviceService:

    def __init__(
        self,
        session: Session,
        device_repo: DeviceRepository,
        admin_user_service: AdminUserService,
        user_institution_service: UserInstitutionService,
        payment_service: PaymentService,
        user_palm_service: UserPalmService,
    ):
        self.session = session
        self.device_repo = device_repo
        self.admin_user_service = admin_user_service
        self.user_institution_service = user_institution_service
        self.payment_service = payment_service
        self.user_palm_service = user_palm_service

    async def verify_palmprint(
        self, data: DeviceVerificationRequest
    ) -> DeviceVerificationResponse:
        # 1. 디바이스 검증
        device = await self._validate_device(data.device_id)

        # 2. 손바닥 임베딩 생성
        try:

            input_embedding = await self.user_palm_service.get_embedding_from_image(
                extract_base64_image(data.palmprint_data)
            )
        except HTTPException as e:
            # 임베딩 생성 실패 시 400 Bad Request
            if e.status_code == status.HTTP_400_BAD_REQUEST:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid palmprint data",
                )
            raise

        # 3. 등록된 손바닥과 매칭
        match_result = await self.user_palm_service.find_matching_user(input_embedding)

        if not match_result.matched:
            return DeviceVerificationResponse(status="false")

        # 4. 유저 정보 조회
        user = await self.admin_user_service.get_user_detail(match_result.user_id)

        # 5. 유저-기관 권한 검증
        await self._validate_user_institution_access(user.id, device.institution_id)

        # 6. 결제 수단 조회 (auth_type이 payment인 경우)
        payment_methods = None
        if data.auth_type == "payment":
            payment_methods = await self.payment_service.get_payment_methods(user.id)

        return DeviceVerificationResponse(
            status="success",
            user=UserCreateResponse(
                id=user.id,
                email=user.email,
                name=user.name,
                phone_number=user.phone_number,
                created_at=user.created_at,
            ),
            payment_method=None,
        )

    async def _validate_device(self, device_id: int) -> Device:
        query = self.device_repo.get_by_id_query(device_id)
        result = await self.session.execute(query)
        device = result.scalar_one_or_none()

        if device is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or unregistered device",
            )

        return device

    async def _validate_user_institution_access(
        self, user_id: int, institution_id: int
    ) -> None:
        try:
            user_institution = await self.user_institution_service.get_institution(
                user_id, institution_id
            )
        except HTTPException as e:
            if e.status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="User not allowed for this institution",
                )
            raise
