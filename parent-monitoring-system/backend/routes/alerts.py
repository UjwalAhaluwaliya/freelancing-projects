from fastapi import APIRouter, Depends

from ..dependencies import ensure_parent_owns_child, get_current_parent_id
from ..services.alert_service import AlertService

router = APIRouter(tags=["alerts"])


@router.get("/alerts/{child_id}")
async def get_alerts(
    child_id: str,
    parent_id: str = Depends(get_current_parent_id),
):
    """Get alerts for a child. Requires parent JWT."""
    await ensure_parent_owns_child(child_id, parent_id)
    alerts = await AlertService.get_alerts(child_id, parent_id)
    return {"child_id": child_id, "alerts": alerts}
