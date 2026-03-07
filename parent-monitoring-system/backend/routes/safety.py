from fastapi import APIRouter, Depends

from ..dependencies import ensure_parent_owns_child, get_current_parent_id
from ..models.safety import CheckUrlRequest, DetectToxicRequest
from ..services.alert_service import AlertService
from ..services.safety_service import SafetyService

router = APIRouter(tags=["safety"])


@router.post("/check-url")
async def check_url(
    body: CheckUrlRequest,
    parent_id: str = Depends(get_current_parent_id),
):
    """Check if URL is safe. If unsafe, block and create alert. Requires parent JWT."""
    await ensure_parent_owns_child(body.child_id, parent_id)
    is_unsafe = SafetyService.check_url_unsafe(body.url)
    if is_unsafe:
        await AlertService.create_alert(
            body.child_id,
            message=f"Blocked website accessed: {body.url}",
            alert_type="blocked_website",
        )
        return {"allowed": False}
    return {"allowed": True}


@router.post("/detect-toxic")
async def detect_toxic(
    body: DetectToxicRequest,
    parent_id: str = Depends(get_current_parent_id),
):
    """Detect toxic words in text. If toxic, create alert. Requires parent JWT."""
    await ensure_parent_owns_child(body.child_id, parent_id)
    is_toxic = SafetyService.detect_toxic(body.text)
    if is_toxic:
        await AlertService.create_alert(
            body.child_id,
            message=f"Toxic message detected: {body.text[:100]}...",
            alert_type="toxic_message",
        )
        return {"toxic": True}
    return {"toxic": False}
