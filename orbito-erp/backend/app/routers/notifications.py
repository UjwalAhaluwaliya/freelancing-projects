from fastapi import APIRouter, HTTPException, Depends
from app.database import supabase
from app.services.auth_dependency import get_current_user

router = APIRouter(prefix="/notifications", tags=["Notifications"])


# ==========================
# GET USER NOTIFICATIONS
# ==========================
@router.get("/")
def get_notifications(user=Depends(get_current_user)):

    user_id = user["user_id"]

    response = supabase.table("notifications") \
        .select("*") \
        .eq("user_id", user_id) \
        .order("created_at", desc=True) \
        .execute()

    return {
        "success": True,
        "data": response.data
    }


# ==========================
# MARK AS READ
# ==========================
@router.put("/{notification_id}/read")
def mark_as_read(notification_id: str, user=Depends(get_current_user)):

    user_id = user["user_id"]

    response = supabase.table("notifications") \
        .update({"is_read": True}) \
        .eq("id", notification_id) \
        .eq("user_id", user_id) \
        .execute()

    return {
        "success": True,
        "message": "Notification marked as read",
        "data": response.data
    }


# ==========================
# UNREAD COUNT
# ==========================
@router.get("/unread-count")
def unread_count(user=Depends(get_current_user)):

    user_id = user["user_id"]

    response = supabase.table("notifications") \
        .select("*", count="exact") \
        .eq("user_id", user_id) \
        .eq("is_read", False) \
        .execute()

    return {
        "success": True,
        "unread_count": response.count
    }