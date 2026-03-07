from fastapi import APIRouter, HTTPException, Depends
from app.services.auth_dependency import hr_or_admin_required
from app.database import supabase
from app.schemas.application_schema import ApplicationCreate, StageUpdate
from app.services.notification_service import create_notification
from app.services.workflow_service import trigger_n8n_workflow
from app.core.config import settings
from datetime import datetime
from passlib.context import CryptContext

router = APIRouter(prefix="/applications", tags=["Applications"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _get_profile_id_from_candidate(candidate_id: str):
    candidate = (
        supabase.table("candidates")
        .select("email")
        .eq("id", candidate_id)
        .execute()
    )
    if not candidate.data:
        return None
    email = candidate.data[0].get("email")
    if not email:
        return None
    profile = (
        supabase.table("profiles")
        .select("id")
        .eq("email", email)
        .execute()
    )
    if not profile.data:
        return None
    return profile.data[0].get("id")


# ==========================
# APPLY FOR JOB
# ==========================
@router.post("/")
async def apply_for_job(application: ApplicationCreate):

    # Check candidate exists
    candidate = supabase.table("candidates") \
        .select("*") \
        .eq("id", str(application.candidate_id)) \
        .execute()

    if not candidate.data:
        raise HTTPException(status_code=404, detail="Candidate not found")

    # Check job exists
    job = supabase.table("job_descriptions") \
        .select("*") \
        .eq("id", str(application.job_id)) \
        .execute()

    if not job.data:
        raise HTTPException(status_code=404, detail="Job not found")

    response = supabase.table("applications").insert({
        "candidate_id": str(application.candidate_id),
        "job_id": str(application.job_id),
        "stage": "applied",
        "stage_updated_at": datetime.utcnow().isoformat()
    }).execute()

    return {
        "success": True,
        "message": "Application submitted successfully",
        "data": response.data
    }


# ==========================
# GET ALL APPLICATIONS
# ==========================
@router.get("/")
async def get_applications(user=Depends(hr_or_admin_required)):

    response = supabase.table("applications") \
        .select("*") \
        .order("created_at", desc=True) \
        .execute()

    return {
        "success": True,
        "data": response.data
    }


# ==========================
# UPDATE STAGE (HR ONLY)
# ==========================
@router.put("/{application_id}/stage")
async def update_stage(
    application_id: str,
    stage_update: StageUpdate,
    user=Depends(hr_or_admin_required)
):
    onboarding_password = None

    valid_stages = [
        "applied",
        "screening",
        "interview",
        "offer",
        "hired",
        "rejected"
    ]

    if stage_update.stage not in valid_stages:
        raise HTTPException(status_code=400, detail="Invalid stage")

    # Fetch current stage + candidate_id
    existing = supabase.table("applications") \
        .select("stage, candidate_id") \
        .eq("id", application_id) \
        .execute()

    if not existing.data:
        raise HTTPException(status_code=404, detail="Application not found")

    current_stage = existing.data[0]["stage"]
    candidate_id = existing.data[0]["candidate_id"]

    # Workflow rules
    allowed_transitions = {
        "applied": ["screening", "rejected"],
        "screening": ["interview", "rejected"],
        "interview": ["offer", "rejected"],
        "offer": ["hired", "rejected"],
        "hired": [],
        "rejected": []
    }

    if stage_update.stage not in allowed_transitions[current_stage]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot move from {current_stage} to {stage_update.stage}"
        )

    # Update stage
    response = supabase.table("applications") \
        .update({
            "stage": stage_update.stage,
            "stage_updated_at": datetime.utcnow().isoformat()
        }) \
        .eq("id", application_id) \
        .execute()

    # ==========================
    # NOTIFY ON STAGE CHANGE
    # ==========================
    if stage_update.stage in ["screening", "interview", "offer", "rejected"]:
        profile_id = _get_profile_id_from_candidate(candidate_id)
        if profile_id:
            create_notification(
                profile_id,
                "Application Update",
                f"Your application moved to {stage_update.stage} stage."
            )

    # HR action acknowledgement
    create_notification(
        user["user_id"],
        "Application Stage Updated",
        f"Application {application_id} moved to {stage_update.stage}."
    )

    # ==========================
    # HIRED LOGIC
    # ==========================
    if stage_update.stage == "hired":

        candidate = supabase.table("candidates") \
            .select("*") \
            .eq("id", candidate_id) \
            .execute()

        if candidate.data:
            candidate_data = candidate.data[0]

            # Create profile if not exists
            existing_profile = supabase.table("profiles") \
                .select("id,email,password,department") \
                .eq("email", candidate_data["email"]) \
                .execute()

            if not existing_profile.data:
                onboarding_password = settings.default_employee_password
                supabase.table("profiles").insert({
                    "email": candidate_data["email"],
                    "full_name": candidate_data["full_name"],
                    "role": "employee",
                    "department": "To Be Assigned",
                    "password": pwd_context.hash(onboarding_password),
                }).execute()
            else:
                existing = existing_profile.data[0]
                patch_data = {}
                if not existing.get("password"):
                    onboarding_password = settings.default_employee_password
                    patch_data["password"] = pwd_context.hash(onboarding_password)
                if not existing.get("department"):
                    patch_data["department"] = "To Be Assigned"
                if patch_data:
                    supabase.table("profiles").update(patch_data).eq("id", existing["id"]).execute()

            # Fetch profile id
            profile = supabase.table("profiles") \
                .select("id") \
                .eq("email", candidate_data["email"]) \
                .execute()

            if profile.data:
                create_notification(
                    profile.data[0]["id"],
                    "Welcome to Orbito ERP",
                    "Congratulations! You have been officially hired."
                )

            create_notification(
                user["user_id"],
                "Candidate Hired",
                f"{candidate_data['full_name']} has been moved to hired stage."
            )

            # 🔥 Trigger n8n workflow
            await trigger_n8n_workflow(
                "candidate_hired",
                {
                    "candidate_id": candidate_id,
                    "email": candidate_data["email"],
                    "name": candidate_data["full_name"]
                }
            )

    return {
        "success": True,
        "message": f"Stage moved from {current_stage} to {stage_update.stage}",
        "data": response.data,
        "onboarding_password": onboarding_password,
    }


# ==========================
# ATS DASHBOARD SUMMARY
# ==========================
@router.get("/dashboard")
async def ats_dashboard(user=Depends(hr_or_admin_required)):

    total_jobs = supabase.table("job_descriptions").select("*", count="exact").execute()
    active_jobs = supabase.table("job_descriptions").select("*", count="exact").eq("status", "active").execute()

    total_candidates = supabase.table("candidates").select("*", count="exact").execute()
    total_applications = supabase.table("applications").select("*", count="exact").execute()

    applied = supabase.table("applications").select("*", count="exact").eq("stage", "applied").execute()
    screening = supabase.table("applications").select("*", count="exact").eq("stage", "screening").execute()
    interview = supabase.table("applications").select("*", count="exact").eq("stage", "interview").execute()
    offer = supabase.table("applications").select("*", count="exact").eq("stage", "offer").execute()
    hired = supabase.table("applications").select("*", count="exact").eq("stage", "hired").execute()
    rejected = supabase.table("applications").select("*", count="exact").eq("stage", "rejected").execute()

    return {
        "success": True,
        "data": {
            "jobs": {
                "total": total_jobs.count,
                "active": active_jobs.count
            },
            "candidates": total_candidates.count,
            "applications": {
                "total": total_applications.count,
                "applied": applied.count,
                "screening": screening.count,
                "interview": interview.count,
                "offer": offer.count,
                "hired": hired.count,
                "rejected": rejected.count
            }
        }
    }
