from datetime import date, datetime
from typing import Optional

from ..database import get_collection
from .alert_service import AlertService
from .screen_time_service import ScreenTimeService


class ReportService:
    """Service for generating reports."""

    @staticmethod
    async def get_report(child_id: str, parent_id: str) -> dict:
        """Get report for a child: daily usage, blocked attempts, screen time."""
        # Verify child belongs to parent
        children_coll = get_collection("children")
        from bson import ObjectId

        child = await children_coll.find_one(
            {"_id": ObjectId(child_id), "parent_id": parent_id}
        )
        if not child:
            return {}

        usage = await ScreenTimeService.get_usage(child_id, parent_id)
        blocked_attempts = await AlertService.count_blocked_attempts(child_id)
        limit_info = await ScreenTimeService.get_limit(child_id, parent_id)

        return {
            "child_id": child_id,
            "daily_usage": usage.get("daily_usage", []),
            "total_usage_minutes": usage.get("total_usage_minutes", 0),
            "blocked_attempts": blocked_attempts,
            "screen_time": {
                "daily_limit": limit_info["daily_limit"] if limit_info else None,
                "limit_set": limit_info is not None,
            },
        }
