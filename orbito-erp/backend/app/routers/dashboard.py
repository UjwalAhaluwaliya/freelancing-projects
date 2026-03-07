from fastapi import APIRouter, Depends, HTTPException
from app.services.auth_dependency import hr_or_admin_required
from app.database import supabase

from datetime import datetime

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


# ==========================
# HR OVERVIEW DASHBOARD
# ==========================
@router.get("/hr-overview")
def hr_overview(role: str = Depends(hr_or_admin_required)):
    try:
        total_employees = supabase.table("profiles") \
            .select("*", count="exact") \
            .eq("role", "employee") \
            .execute()

        total_candidates = supabase.table("candidates") \
            .select("*", count="exact") \
            .execute()

        active_jobs = supabase.table("job_descriptions") \
            .select("*", count="exact") \
            .eq("status", "active") \
            .execute()

        total_hires = supabase.table("applications") \
            .select("*", count="exact") \
            .eq("stage", "hired") \
            .execute()

        total_interviews = supabase.table("interviews") \
            .select("*", count="exact") \
            .execute()

        return {
            "success": True,
            "data": {
                "employees": total_employees.count,
                "candidates": total_candidates.count,
                "active_jobs": active_jobs.count,
                "total_hires": total_hires.count,
                "total_interviews": total_interviews.count
            }
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==========================
# PERFORMANCE ANALYTICS
# ==========================
@router.get("/performance")
def performance_dashboard(role: str = Depends(hr_or_admin_required)):
    try:
        achievements = supabase.table("achievements") \
            .select("user_id, points") \
            .execute()

        user_points = {}

        for row in achievements.data:
            user_points[row["user_id"]] = user_points.get(row["user_id"], 0) + row["points"]

        if not user_points:
            return {"success": True, "data": {}}

        # Top performer
        top_user_id = max(user_points, key=user_points.get)
        top_points = user_points[top_user_id]

        profile = supabase.table("profiles") \
            .select("full_name") \
            .eq("id", top_user_id) \
            .execute()

        top_name = profile.data[0]["full_name"] if profile.data else "Unknown"

        return {
            "success": True,
            "data": {
                "top_performer": {
                    "user_id": top_user_id,
                    "full_name": top_name,
                    "points": top_points
                }
            }
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==========================
# SYSTEM HEALTH
# ==========================
@router.get("/system-health")
def system_health(role: str = Depends(hr_or_admin_required)):
    try:
        pending_leaves = supabase.table("leave_requests") \
            .select("*", count="exact") \
            .eq("status", "pending") \
            .execute()

        pending_applications = supabase.table("applications") \
            .select("*", count="exact") \
            .eq("stage", "applied") \
            .execute()

        today = datetime.utcnow().date()

        interviews_today = supabase.table("interviews") \
            .select("*") \
            .execute()

        today_count = 0

        for interview in interviews_today.data:
            if interview["interview_date"]:
                interview_date = datetime.fromisoformat(interview["interview_date"]).date()
                if interview_date == today:
                    today_count += 1

        return {
            "success": True,
            "data": {
                "pending_leaves": pending_leaves.count,
                "pending_applications": pending_applications.count,
                "interviews_today": today_count
            }
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))