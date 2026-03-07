from fastapi import APIRouter, HTTPException, Depends
from app.services.auth_dependency import hr_or_admin_required
from app.database import supabase
from app.schemas.job_schema import JobCreate, JobUpdate


router = APIRouter(prefix="/jobs", tags=["Jobs"])


# ==========================
# CREATE JOB
# ==========================
@router.post("/")
def create_job(job: JobCreate, role: str = Depends(hr_or_admin_required)):
    try:
        response = supabase.table("job_descriptions").insert({
            "title": job.title,
            "department_id": str(job.department_id) if job.department_id else None,
            "experience_level": job.experience_level,
            "location": job.location,
            "employment_type": job.employment_type,
            "description": job.description
        }).execute()

        return {
            "success": True,
            "message": "Job created successfully",
            "data": response.data
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==========================
# GET ALL JOBS
# ==========================
@router.get("/")
def get_jobs():
    response = supabase.table("job_descriptions").select("*").execute()

    return {
        "success": True,
        "data": response.data
    }


# ==========================
# UPDATE JOB
# ==========================
@router.put("/{job_id}")
def update_job(job_id: str, job: JobUpdate, role: str = Depends(hr_or_admin_required)):
    try:
        update_data = {k: v for k, v in job.dict().items() if v is not None}

        response = supabase.table("job_descriptions") \
            .update(update_data) \
            .eq("id", job_id) \
            .execute()

        return {
            "success": True,
            "message": "Job updated successfully",
            "data": response.data
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==========================
# DELETE JOB
# ==========================
@router.delete("/{job_id}")
def delete_job(job_id: str, role: str = Depends(hr_or_admin_required)):
    try:
        response = supabase.table("job_descriptions") \
            .delete() \
            .eq("id", job_id) \
            .execute()

        return {
            "success": True,
            "message": "Job deleted successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))