from datetime import datetime
from typing import List, Optional

from bson import ObjectId

from ..database import get_collection

ALERTS_COLLECTION = "alerts"


class AlertService:
    """Service for alert operations."""

    @staticmethod
    async def create_alert(
        child_id: str,
        message: str,
        alert_type: Optional[str] = None,
    ) -> dict:
        """Create a new alert."""
        coll = get_collection(ALERTS_COLLECTION)
        doc = {
            "child_id": child_id,
            "message": message,
            "timestamp": datetime.utcnow(),
        }
        if alert_type:
            doc["alert_type"] = alert_type
        result = await coll.insert_one(doc)
        doc["id"] = str(result.inserted_id)
        return doc

    @staticmethod
    async def get_alerts(child_id: str, parent_id: str, limit: int = 100) -> List[dict]:
        """Get alerts for a child. Verifies child belongs to parent via children collection."""
        children_coll = get_collection("children")
        child = await children_coll.find_one(
            {"_id": ObjectId(child_id), "parent_id": parent_id}
        )
        if not child:
            return []
        alerts_coll = get_collection(ALERTS_COLLECTION)
        cursor = (
            alerts_coll.find({"child_id": child_id})
            .sort("timestamp", -1)
            .limit(limit)
        )
        alerts = []
        async for doc in cursor:
            alerts.append(
                {
                    "id": str(doc["_id"]),
                    "child_id": doc["child_id"],
                    "message": doc["message"],
                    "timestamp": doc["timestamp"].isoformat()
                    if hasattr(doc["timestamp"], "isoformat")
                    else str(doc["timestamp"]),
                    "alert_type": doc.get("alert_type"),
                }
            )
        return alerts

    @staticmethod
    async def count_blocked_attempts(child_id: str) -> int:
        """Count blocked website attempts for a child."""
        coll = get_collection(ALERTS_COLLECTION)
        return await coll.count_documents(
            {"child_id": child_id, "alert_type": "blocked_website"}
        )
