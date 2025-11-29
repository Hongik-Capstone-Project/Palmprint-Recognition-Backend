from fastapi import APIRouter, status

router = APIRouter(prefix="/api/admin/reports", tags=["Admin-Reports"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_reports():
    pass


@router.get("/{report_id}", status_code=status.HTTP_200_OK)
async def get_report_detail(report_id: int):
    pass


@router.patch("/{report_id}/status", status_code=status.HTTP_200_OK)
async def update_report_status(report_id: int):
    pass
