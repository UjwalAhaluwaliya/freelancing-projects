from fastapi import APIRouter, HTTPException, Depends
from app.services.auth_dependency import hr_or_admin_required
from app.database import supabase
from app.schemas.interview_schema import InterviewCreate, InterviewUpdate

from app.services.notification_service import create_notification
from app.services.achievement_service import add_points

router = APIRouter(prefix="/interviews", tags=["Interviews"])


# ==========================
# SCHEDULE INTERVIEW
# ==========================
@router.post("/")
def schedule_interview(interview: InterviewCreate, role: str = Depends(hr_or_admin_required)):
    try:
        response = supabase.table("interviews").insert({
            "application_id": str(interview.application_id),
            "interviewer_name": interview.interviewer_name,
            "interview_date": interview.interview_date.isoformat(),
            "status": "scheduled"
        }).execute()

        # 🔔 Notify candidate
        application = supabase.table("applications") \
            .select("candidate_id") \
            .eq("id", str(interview.application_id)) \
            .execute()

        if application.data:
            candidate_id = application.data[0]["candidate_id"]

            candidate = supabase.table("candidates") \
                .select("email") \
                .eq("id", candidate_id) \
                .execute()

            if candidate.data:
                profile = supabase.table("profiles") \
                    .select("id") \
                    .eq("email", candidate.data[0]["email"]) \
                    .execute()

                if profile.data:
                    create_notification(
                        profile.data[0]["id"],
                        "Interview Scheduled",
                        f"Your interview is scheduled on {interview.interview_date}"
                    )

        return {
            "success": True,
            "message": "Interview scheduled successfully",
            "data": response.data
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==========================
# UPDATE INTERVIEW
# ==========================
@router.put("/{interview_id}")
def update_interview(interview_id: str, interview: InterviewUpdate, role: str = Depends(hr_or_admin_required)):
    try:
        update_data = {k: v for k, v in interview.dict().items() if v is not None}

        response = supabase.table("interviews") \
            .update(update_data) \
            .eq("id", interview_id) \
            .execute()

        # 🎯 If interview completed → notify + add points
        if "status" in update_data and update_data["status"] == "completed":

            interview_data = supabase.table("interviews") \
                .select("application_id") \
                .eq("id", interview_id) \
                .execute()

            if interview_data.data:
                application_id = interview_data.data[0]["application_id"]

                application = supabase.table("applications") \
                    .select("candidate_id") \
                    .eq("id", application_id) \
                    .execute()

                if application.data:
                    candidate_id = application.data[0]["candidate_id"]

                    candidate = supabase.table("candidates") \
                        .select("email") \
                        .eq("id", candidate_id) \
                        .execute()

                    if candidate.data:
                        profile = supabase.table("profiles") \
                            .select("id") \
                            .eq("email", candidate.data[0]["email"]) \
                            .execute()

                        if profile.data:
                            user_id = profile.data[0]["id"]

                            # 🔔 Notification
                            create_notification(
                                user_id,
                                "Interview Completed",
                                "Your interview has been completed. HR will contact you soon."
                            )

                            # 🏆 +10 Points
                            add_points(
                                user_id,
                                10,
                                "Interview completed successfully"
                            )

        return {
            "success": True,
            "message": "Interview updated successfully",
            "data": response.data
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==========================
# GET ALL INTERVIEWS
# ==========================
@router.get("/")
def get_interviews(role: str = Depends(hr_or_admin_required)):
    response = supabase.table("interviews").select("*").execute()

    return {
        "success": True,
        "data": response.data
    }