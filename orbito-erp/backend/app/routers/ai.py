from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
import httpx
from uuid import UUID
from typing import Optional
from app.database import supabase
from app.schemas.ai_schema import (
    JobDescriptionRequest,
    ResumeScoreRequest,
    PolicyChatRequest,
)
from app.services.ai_service import (
    generate_job_description,
    score_resume,
    policy_chatbot,
    extract_text_from_pdf_bytes,
    AIQuotaExceededError,
    generate_job_description_local,
    score_resume_local,
    policy_chatbot_local,
)
from app.services.auth_dependency import hr_or_admin_required
from app.services.shortlist_service import trigger_resume_shortlist_automation
from app.core.config import settings

router = APIRouter(prefix="/ai", tags=["AI"])


async def _handle_resume_scoring(
    *,
    user_id: str,
    resume_text: str,
    job_description: str,
    shortlist_threshold: int,
    candidate_id: Optional[UUID] = None,
    application_id: Optional[UUID] = None,
):
    try:
        analysis = await score_resume(resume_text, job_description)
        ai_source = "gemini"
    except AIQuotaExceededError:
        analysis = score_resume_local(resume_text, job_description)
        ai_source = "local-fallback"
    score = analysis["match_score"]
    shortlisted = score >= shortlist_threshold

    if candidate_id:
        try:
            supabase.table("candidates").update(
                {
                    "overall_score": score,
                    "recommendation": analysis["recommendation"],
                }
            ).eq("id", str(candidate_id)).execute()
        except Exception:
            pass

    if shortlisted:
        automation_result = await trigger_resume_shortlist_automation(
            candidate_id=str(candidate_id) if candidate_id else None,
            application_id=str(application_id) if application_id else None,
            analysis=analysis,
            threshold=shortlist_threshold,
            hr_user_id=user_id,
        )
        workflow_result = automation_result["workflow"]
        workflow_payload = automation_result["payload"]
    else:
        workflow_result = {
            "ok": True,
            "status_code": None,
            "error": None,
            "message": "Threshold not met, workflow not triggered",
        }
        workflow_payload = None

    return {
        "success": True,
        "ai_source": ai_source,
        "shortlisted": shortlisted,
        "threshold": shortlist_threshold,
        "analysis": analysis,
        "workflow": workflow_result,
        "workflow_payload": workflow_payload,
    }


@router.post("/generate-job")
async def ai_generate_job(payload: JobDescriptionRequest, user=Depends(hr_or_admin_required)):
    try:
        result = await generate_job_description(
            payload.title,
            payload.skills,
            payload.experience,
            payload.department,
        )
        source = "gemini"
    except AIQuotaExceededError:
        result = generate_job_description_local(
            payload.title,
            payload.skills,
            payload.experience,
            payload.department,
        )
        source = "local-fallback"
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"AI generation failed: {exc}") from exc
    return {"success": True, "source": source, "job_description": result}


@router.post("/score-resume")
async def ai_score_resume(payload: ResumeScoreRequest, user=Depends(hr_or_admin_required)):
    try:
        return await _handle_resume_scoring(
            user_id=user["user_id"],
            resume_text=payload.resume_text,
            job_description=payload.job_description,
            shortlist_threshold=payload.shortlist_threshold,
            candidate_id=payload.candidate_id,
            application_id=payload.application_id,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Resume scoring failed: {exc}") from exc


@router.post("/score-resume-pdf")
async def ai_score_resume_pdf(
    user=Depends(hr_or_admin_required),
    resume_file: UploadFile = File(...),
    job_description: str = Form(...),
    shortlist_threshold: int = Form(70),
    candidate_id: Optional[UUID] = Form(None),
    application_id: Optional[UUID] = Form(None),
):
    if not resume_file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF resumes are supported")

    file_bytes = await resume_file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded resume file is empty")

    try:
        resume_text = extract_text_from_pdf_bytes(file_bytes)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Unable to parse PDF: {exc}") from exc

    if len(resume_text.strip()) < 20:
        raise HTTPException(
            status_code=400,
            detail="Resume PDF has insufficient extractable text",
        )

    try:
        return await _handle_resume_scoring(
            user_id=user["user_id"],
            resume_text=resume_text,
            job_description=job_description,
            shortlist_threshold=shortlist_threshold,
            candidate_id=candidate_id,
            application_id=application_id,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Resume scoring failed: {exc}") from exc


@router.post("/policy-chat")
async def ai_policy_chat(payload: PolicyChatRequest):
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(
                settings.policy_chat_webhook_url,
                json={"question": payload.question},
            )
            response.raise_for_status()
            return response.json()
    except Exception:
        try:
            fallback = await policy_chatbot(payload.question)
            if fallback:
                return {"success": True, "reply": fallback, "source": "gemini-fallback"}
        except AIQuotaExceededError:
            pass
        except Exception:
            pass
        local_reply = policy_chatbot_local(payload.question)
        return {"success": True, "reply": local_reply, "source": "local-fallback"}
