from fastapi.testclient import TestClient
from app.main import app
from app.services.jwt_service import create_access_token


def _auth_headers(role: str = "hr"):
    token = create_access_token({"user_id": "test-hr-user", "role": role})
    return {"Authorization": f"Bearer {token}"}


def test_score_resume_shortlisted_triggers_automation(monkeypatch):
    async def fake_score_resume(resume_text, job_description):
        return {
            "match_score": 88,
            "strengths": ["Python"],
            "missing_skills": ["K8s"],
            "recommendation": "Hire",
            "summary": "Strong fit",
            "raw_output": "{}",
        }

    async def fake_automation(**kwargs):
        return {
            "workflow": {"ok": True, "status_code": 200, "error": None},
            "payload": {"event_version": "1.0", "analysis": {"match_score": 88}},
        }

    monkeypatch.setattr("app.routers.ai.score_resume", fake_score_resume)
    monkeypatch.setattr(
        "app.routers.ai.trigger_resume_shortlist_automation",
        fake_automation,
    )

    client = TestClient(app)
    response = client.post(
        "/ai/score-resume",
        json={
            "resume_text": "A" * 60,
            "job_description": "B" * 60,
            "shortlist_threshold": 70,
        },
        headers=_auth_headers(),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["shortlisted"] is True
    assert body["workflow"]["ok"] is True
    assert body["workflow_payload"]["event_version"] == "1.0"


def test_score_resume_below_threshold_skips_automation(monkeypatch):
    async def fake_score_resume(resume_text, job_description):
        return {
            "match_score": 40,
            "strengths": [],
            "missing_skills": ["Python"],
            "recommendation": "Reject",
            "summary": "Weak fit",
            "raw_output": "{}",
        }

    async def fail_if_called(**kwargs):
        raise AssertionError("Automation should not be called for low score")

    monkeypatch.setattr("app.routers.ai.score_resume", fake_score_resume)
    monkeypatch.setattr(
        "app.routers.ai.trigger_resume_shortlist_automation",
        fail_if_called,
    )

    client = TestClient(app)
    response = client.post(
        "/ai/score-resume",
        json={
            "resume_text": "A" * 60,
            "job_description": "B" * 60,
            "shortlist_threshold": 70,
        },
        headers=_auth_headers(),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["shortlisted"] is False
    assert body["workflow_payload"] is None
