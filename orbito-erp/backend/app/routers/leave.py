from fastapi import APIRouter, HTTPException, Depends
from app.services.auth_dependency import hr_or_admin_required, employee_required
from app.database import supabase
from app.schemas.leave_schema import LeaveCreate
from app.services.notification_service import create_notification
from app.services.achievement_service import add_points
from datetime import datetime

router = APIRouter(prefix="/leave", tags=["Leave"])


@router.get("/")
def get_leave_requests(user=Depends(hr_or_admin_required)):
    response = (
        supabase.table("leave_requests")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )
    return {"success": True, "data": response.data}


@router.get("/my")
def get_my_leave_requests(user=Depends(employee_required)):
    response = (
        supabase.table("leave_requests")
        .select("*")
        .eq("employee_id", user["user_id"])
        .order("created_at", desc=True)
        .execute()
    )
    return {"success": True, "data": response.data}


# ==========================
# APPLY LEAVE
# ==========================
@router.post("/")
def apply_leave(leave: LeaveCreate, user=Depends(employee_required)):

    start = datetime.strptime(str(leave.start_date), "%Y-%m-%d")
    end = datetime.strptime(str(leave.end_date), "%Y-%m-%d")

    if end < start:
        raise HTTPException(status_code=400, detail="End date cannot be before start date")

    days = (end - start).days + 1

    response = supabase.table("leave_requests").insert({
        "employee_id": leave.employee_id,
        "leave_type": leave.leave_type,
        "start_date": str(leave.start_date),
        "end_date": str(leave.end_date),
        "days_requested": days,
        "reason": leave.reason,
        "status": "pending"
    }).execute()

    create_notification(
        leave.employee_id,
        "Leave Applied",
        f"You applied for {leave.leave_type} leave from {leave.start_date} to {leave.end_date}"
    )

    return {
        "success": True,
        "message": "Leave applied successfully",
        "data": response.data
    }


# ==========================
# APPROVE LEAVE
# ==========================
@router.put("/approve/{leave_id}")
def approve_leave(leave_id: str, user=Depends(hr_or_admin_required)):

    leave = supabase.table("leave_requests") \
        .select("*") \
        .eq("id", leave_id) \
        .execute()

    if not leave.data:
        raise HTTPException(status_code=404, detail="Leave not found")

    if leave.data[0]["status"] != "pending":
        raise HTTPException(status_code=400, detail="Leave already processed")

    response = supabase.table("leave_requests") \
        .update({"status": "approved"}) \
        .eq("id", leave_id) \
        .execute()

    employee_id = leave.data[0]["employee_id"]

    # 🔔 Notification
    create_notification(
        employee_id,
        "Leave Approved",
        "Your leave request has been approved"
    )

    # 🏆 Achievement Points
    add_points(
        employee_id,
        5,
        "Leave approved successfully"
    )

    return {
        "success": True,
        "message": "Leave approved successfully",
        "data": response.data
    }


# ==========================
# REJECT LEAVE
# ==========================
@router.put("/reject/{leave_id}")
def reject_leave(leave_id: str, user=Depends(hr_or_admin_required)):

    leave = supabase.table("leave_requests") \
        .select("*") \
        .eq("id", leave_id) \
        .execute()

    if not leave.data:
        raise HTTPException(status_code=404, detail="Leave not found")

    if leave.data[0]["status"] != "pending":
        raise HTTPException(status_code=400, detail="Leave already processed")

    response = supabase.table("leave_requests") \
        .update({"status": "rejected"}) \
        .eq("id", leave_id) \
        .execute()

    create_notification(
        leave.data[0]["employee_id"],
        "Leave Rejected",
        "Your leave request has been rejected"
    )

    return {
        "success": True,
        "message": "Leave rejected successfully",
        "data": response.data
    }
