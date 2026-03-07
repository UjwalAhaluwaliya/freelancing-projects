from datetime import datetime, timezone
from typing import Any, Dict, Optional
from app.database import supabase
from app.schemas.workflow_schema import ResumeShortlistPayload
from app.services.notification_service import create_notification
from app.services.workflow_service import trigger_n8n_workflow


def build_resume_shortlist_payload(
    *,
    candidate_id: Optional[str],
    application_id: Optional[str],
    analysis: Dict[str, Any],
    threshold: int,
    hr_user_id: str,
    candidate_record: Optional[Dict[str, Any]] = None,
    application_record: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    return {
        "event_version": "1.0",
        "triggered_at": datetime.now(timezone.utc).isoformat(),
        "threshold": threshold,
        "hr_user_id": hr_user_id,
        "candidate": {
            "id": candidate_id,
            "full_name": (candidate_record or {}).get("full_name"),
            "email": (candidate_record or {}).get("email"),
            "phone": (candidate_record or {}).get("phone"),
        },
        "application": {
            "id": application_id,
            "stage": (application_record or {}).get("stage"),
            "job_id": (application_record or {}).get("job_id"),
            "candidate_id": (application_record or {}).get("candidate_id"),
        },
        "analysis": {
            "match_score": analysis.get("match_score", 0),
            "recommendation": analysis.get("recommendation", "Consider"),
            "summary": analysis.get("summary", ""),
            "strengths": analysis.get("strengths", []),
            "missing_skills": analysis.get("missing_skills", []),
            "raw_output": analysis.get("raw_output", ""),
        },
    }


async def trigger_resume_shortlist_automation(
    *,
    candidate_id: Optional[str],
    application_id: Optional[str],
    analysis: Dict[str, Any],
    threshold: int,
    hr_user_id: str,
) -> Dict[str, Any]:
    candidate_record = None
    application_record = None

    if candidate_id:
        candidate_query = supabase.table("candidates").select("*").eq("id", candidate_id).execute()
        if candidate_query.data:
            candidate_record = candidate_query.data[0]

    if application_id:
        application_query = (
            supabase.table("applications").select("*").eq("id", application_id).execute()
        )
        if application_query.data:
            application_record = application_query.data[0]

    payload_raw = build_resume_shortlist_payload(
        candidate_id=candidate_id,
        application_id=application_id,
        analysis=analysis,
        threshold=threshold,
        hr_user_id=hr_user_id,
        candidate_record=candidate_record,
        application_record=application_record,
    )
    payload = ResumeShortlistPayload.model_validate(payload_raw).model_dump()

    workflow_result = await trigger_n8n_workflow("resume_shortlisted", payload)

    create_notification(
        hr_user_id,
        "Resume Shortlisted",
        f"Shortlist workflow triggered (score: {analysis.get('match_score', 0)}).",
    )

    return {
        "workflow": workflow_result,
        "payload": payload,
    }
