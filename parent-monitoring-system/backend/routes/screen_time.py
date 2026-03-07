from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import (
    ensure_parent_owns_child,
    get_current_parent_id,
    get_current_child_id,
)

from ..models.screen_time_limit import (
    LogUsageRequest,
    ResetUsageRequest,
    SetLimitRequest
)

from ..services.screen_time_service import ScreenTimeService


router = APIRouter(tags=["screen-time"])


# ===============================
# Parent - Set Limit
# ===============================
@router.post("/set-limit")
async def set_limit(
    body: SetLimitRequest,
    parent_id: str = Depends(get_current_parent_id),
):

    await ensure_parent_owns_child(
        body.child_id,
        parent_id
    )

    result = await ScreenTimeService.set_daily_limit(
        body.child_id,
        body.daily_limit,
        parent_id
    )

    return {
        "message": "Limit set successfully",
        **result
    }


# ===============================
# Parent - Get Usage
# ===============================
@router.get("/usage/{child_id}")
async def get_usage(
    child_id: str,
    parent_id: str = Depends(get_current_parent_id),
):

    await ensure_parent_owns_child(
        child_id,
        parent_id
    )

    usage = await ScreenTimeService.get_usage(
        child_id,
        parent_id
    )

    return usage


@router.post("/reset-usage")
async def reset_usage(
    body: ResetUsageRequest,
    parent_id: str = Depends(get_current_parent_id),
):
    await ensure_parent_owns_child(
        body.child_id,
        parent_id,
    )

    result = await ScreenTimeService.reset_usage(
        body.child_id,
        parent_id,
        body.date,
    )

    return {
        "message": "Usage reset successfully",
        **result,
    }


# ===============================
# Child - Log Usage
# ===============================
@router.post("/log-usage")
async def log_usage(
    body: LogUsageRequest,
    child_id: str = Depends(get_current_child_id),
):

    try:

        date_val = datetime.strptime(
            body.date,
            "%Y-%m-%d"
        )

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Invalid date format"
        )

    total, exceeded = await ScreenTimeService.add_usage(

        child_id,
        date_val,
        body.usage_time

    )

    return {
        "usage_time": total,
        "limit_exceeded": exceeded
    }
