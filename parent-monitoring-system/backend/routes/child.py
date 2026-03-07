"""Child-facing API routes. All require child JWT."""

from datetime import date

from fastapi import APIRouter, Depends

from ..dependencies import get_current_child_id
from ..models.safety import ChildCheckUrlRequest
from ..services.alert_service import AlertService
from ..services.safety_service import SafetyService
from ..database import get_collection

router = APIRouter(prefix="/child", tags=["child"])


@router.post("/check-url")
async def child_check_url(
    body: ChildCheckUrlRequest,
    child_id: str = Depends(get_current_child_id),
):
    """Check if URL is safe. Uses child_id from JWT."""
    today_str = date.today().isoformat()
    usage_coll = get_collection("usage_logs")
    usage_doc = await usage_coll.find_one(
        {"child_id": child_id, "date": today_str}
    )
    today_usage = usage_doc["usage_time"] if usage_doc else 0

    limit_coll = get_collection("screen_time")
    limit_doc = await limit_coll.find_one({"child_id": child_id})
    daily_limit = limit_doc["daily_limit"] if limit_doc else None

    if daily_limit is not None and today_usage >= daily_limit:
        return {"allowed": False, "reason": "time_limit"}

    is_unsafe = SafetyService.check_url_unsafe(body.url)
    if is_unsafe:
        await AlertService.create_alert(
            child_id,
            message=f"Blocked website accessed: {body.url}",
            alert_type="blocked_website",
        )
        return {"allowed": False, "reason": "unsafe_url"}
    return {"allowed": True}


@router.get("/usage")
async def child_get_usage(child_id: str = Depends(get_current_child_id)):
    """Get usage for the authenticated child."""
    coll = get_collection("usage_logs")
    cursor = coll.find({"child_id": child_id}).sort("date", -1).limit(30)
    daily_usage = []
    total = 0
    async for doc in cursor:
        date_str = (
            doc["date"].isoformat()
            if hasattr(doc["date"], "isoformat")
            else str(doc["date"])
        )
        daily_usage.append({"date": date_str, "usage_time": doc["usage_time"]})
        total += doc["usage_time"]
    return {
        "child_id": child_id,
        "daily_usage": daily_usage,
        "total_usage_minutes": total,
    }




@router.get("/dashboard")
async def child_dashboard(child_id: str = Depends(get_current_child_id)):

    today_str = date.today().isoformat()

    usage_coll = get_collection("usage_logs")

    usage_doc = await usage_coll.find_one({
        "child_id": child_id,
        "date": today_str
    })

    today_usage = usage_doc["usage_time"] if usage_doc else 0


    limit_coll = get_collection("screen_time")

    limit_doc = await limit_coll.find_one({
        "child_id": child_id
    })

    daily_limit = limit_doc["daily_limit"] if limit_doc else None


    remaining = None

    if daily_limit is not None:
        remaining = max(0, daily_limit - today_usage)


    return {
        "child_id": child_id,
        "daily_limit": daily_limit,
        "today_usage_minutes": today_usage,
        "remaining_minutes": remaining,
        "limit_exceeded": daily_limit is not None and today_usage >= daily_limit
    }

@router.post("/log-usage")
async def log_usage(body: dict, child_id: str = Depends(get_current_child_id)):
    """Increments usage time for the child. Called every minute from the app."""
    today_str = date.today().isoformat()
    coll = get_collection("usage_logs")
    
    # Increment usage_time by 1 for the specific child and date
    await coll.update_one(
        {"child_id": child_id, "date": today_str},
        {"$inc": {"usage_time": 1}},
        upsert=True
    )
    
    # Check if they just hit the limit
    limit_coll = get_collection("screen_time")
    limit_doc = await limit_coll.find_one({"child_id": child_id})
    
    if limit_doc:
        new_usage_doc = await coll.find_one({"child_id": child_id, "date": today_str})
        if new_usage_doc["usage_time"] >= limit_doc["daily_limit"]:
            return {"status": "success", "limit_exceeded": True}
            
    return {"status": "success", "limit_exceeded": False}
