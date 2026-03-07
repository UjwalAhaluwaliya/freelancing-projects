from datetime import date, datetime
from ..database import get_collection

SCREEN_TIME_COLLECTION = "screen_time"
USAGE_LOGS_COLLECTION = "usage_logs"


class ScreenTimeService:

    # ==========================
    # Set Screen Limit
    # ==========================
    @staticmethod
    async def set_daily_limit(child_id: str, daily_limit: int, parent_id: str):

        coll = get_collection(SCREEN_TIME_COLLECTION)

        # Treat 0 (or negative guard) as "remove limit".
        if daily_limit <= 0:
            await coll.delete_one(
                {
                    "child_id": child_id,
                    "parent_id": parent_id,
                }
            )
            return {
                "child_id": child_id,
                "daily_limit": None,
                "limit_removed": True,
            }

        await coll.update_one(
            {
                "child_id": child_id,
                "parent_id": parent_id
            },
            {
                "$set": {
                    "child_id": child_id,
                    "parent_id": parent_id,
                    "daily_limit": daily_limit,
                    "updated_at": datetime.utcnow()
                }
            },
            upsert=True
        )

        return {
            "child_id": child_id,
            "daily_limit": daily_limit,
            "limit_removed": False,
        }


    # ==========================
    # Get Limit
    # ==========================
    @staticmethod
    async def get_limit(child_id: str, parent_id: str = None):

        coll = get_collection(SCREEN_TIME_COLLECTION)

        query = {"child_id": child_id}

        if parent_id:
            query["parent_id"] = parent_id

        doc = await coll.find_one(query)

        if not doc:
            return None

        return {
            "child_id": child_id,
            "daily_limit": doc["daily_limit"]
        }


    # ==========================
    # ADD USAGE (Child App)
    # ==========================
    @staticmethod
    async def add_usage(child_id: str, date_val, usage_minutes: int):

        coll = get_collection(USAGE_LOGS_COLLECTION)

        result = await coll.find_one_and_update(

            {
                "child_id": child_id,
                "date": date_val.isoformat()
            },

            {
                "$inc": {
                    "usage_time": usage_minutes
                }
            },

            upsert=True,
            return_document=True
        )

        total = result.get("usage_time", 0)

        limit_doc = await get_collection(
            SCREEN_TIME_COLLECTION
        ).find_one({
            "child_id": child_id
        })

        limit = None

        if limit_doc:
            limit = limit_doc.get("daily_limit")

        exceeded = False

        if limit:
            exceeded = total >= limit

        return total, exceeded


    # ==========================
    # GET USAGE
    # ==========================
    @staticmethod
    async def get_usage(child_id: str, parent_id: str = None):

        coll = get_collection(USAGE_LOGS_COLLECTION)

        cursor = coll.find({
            "child_id": child_id
        }).sort("date", -1).limit(30)

        daily_usage = []
        total = 0

        async for doc in cursor:

            minutes = doc.get("usage_time", 0)

            daily_usage.append({
                "date": str(doc["date"]),
                "usage_time": minutes
            })

            total += minutes

        return {
            "child_id": child_id,
            "daily_usage": daily_usage,
            "total_usage_minutes": total
        }

    # ==========================
    # RESET USAGE
    # ==========================
    @staticmethod
    async def reset_usage(child_id: str, parent_id: str, date_str: str | None = None):
        target_date = date_str or date.today().isoformat()

        coll = get_collection(USAGE_LOGS_COLLECTION)
        await coll.update_one(
            {"child_id": child_id, "date": target_date},
            {
                "$set": {
                    "child_id": child_id,
                    "date": target_date,
                    "usage_time": 0,
                    "updated_at": datetime.utcnow(),
                }
            },
            upsert=True,
        )

        limit_doc = await get_collection(SCREEN_TIME_COLLECTION).find_one(
            {"child_id": child_id, "parent_id": parent_id}
        )
        daily_limit = limit_doc.get("daily_limit") if limit_doc else None
        remaining = daily_limit if daily_limit is not None else None

        return {
            "child_id": child_id,
            "date": target_date,
            "usage_time": 0,
            "daily_limit": daily_limit,
            "remaining_minutes": remaining,
            "limit_exceeded": False,
        }
