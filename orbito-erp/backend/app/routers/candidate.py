from fastapi import APIRouter, HTTPException, Depends
from app.services.auth_dependency import hr_or_admin_required
from app.database import supabase
from app.schemas.candidate_schema import CandidateCreate, CandidateUpdate


router = APIRouter(prefix="/candidates", tags=["Candidates"])


# ==========================
# CREATE CANDIDATE
# ==========================
@router.post("/")
def create_candidate(candidate: CandidateCreate):
    try:
        response = supabase.table("candidates").insert({
            "full_name": candidate.full_name,
            "email": candidate.email,
            "phone": candidate.phone,
            "skills": candidate.skills,
            "total_experience": candidate.total_experience,
            "resume_url": candidate.resume_url
        }).execute()

        return {
            "success": True,
            "message": "Candidate created successfully",
            "data": response.data
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==========================
# GET ALL CANDIDATES
# ==========================
@router.get("/")
def get_candidates():
    response = supabase.table("candidates").select("*").execute()

    return {
        "success": True,
        "data": response.data
    }


# ==========================
# UPDATE CANDIDATE
# ==========================
@router.put("/{candidate_id}")
def update_candidate(candidate_id: str, candidate: CandidateUpdate, role: str = Depends(hr_or_admin_required)):
    try:
        update_data = {k: v for k, v in candidate.dict().items() if v is not None}

        response = supabase.table("candidates") \
            .update(update_data) \
            .eq("id", candidate_id) \
            .execute()

        return {
            "success": True,
            "message": "Candidate updated successfully",
            "data": response.data
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==========================
# DELETE CANDIDATE
# ==========================
@router.delete("/{candidate_id}")
def delete_candidate(candidate_id: str, role: str = Depends(hr_or_admin_required)):
    try:
        supabase.table("candidates") \
            .delete() \
            .eq("id", candidate_id) \
            .execute()

        return {
            "success": True,
            "message": "Candidate deleted successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))