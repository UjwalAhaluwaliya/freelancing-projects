from fastapi import APIRouter, Depends

from ..dependencies import ensure_parent_owns_child, get_current_parent_id
from ..services.report_service import ReportService

router = APIRouter(tags=["reports"])


@router.get("/reports/{child_id}")
async def get_report(
    child_id: str,
    parent_id: str = Depends(get_current_parent_id),
):
    """Get report for a child: daily usage, blocked attempts, screen time. Requires parent JWT."""
    await ensure_parent_owns_child(child_id, parent_id)
    report = await ReportService.get_report(child_id, parent_id)
    return report
