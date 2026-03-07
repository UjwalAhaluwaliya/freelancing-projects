from app.services.shortlist_service import build_resume_shortlist_payload


def test_build_resume_shortlist_payload_contains_contract_fields():
    payload = build_resume_shortlist_payload(
        candidate_id="candidate-1",
        application_id="application-1",
        analysis={
            "match_score": 88,
            "recommendation": "Hire",
            "summary": "Strong match",
            "strengths": ["FastAPI"],
            "missing_skills": ["React"],
            "raw_output": "raw",
        },
        threshold=70,
        hr_user_id="hr-1",
        candidate_record={
            "full_name": "Aman Kumar",
            "email": "aman@example.com",
            "phone": "9999999999",
        },
        application_record={
            "stage": "screening",
            "job_id": "job-1",
            "candidate_id": "candidate-1",
        },
    )

    assert payload["event_version"] == "1.0"
    assert payload["threshold"] == 70
    assert payload["hr_user_id"] == "hr-1"
    assert payload["candidate"]["id"] == "candidate-1"
    assert payload["application"]["id"] == "application-1"
    assert payload["analysis"]["match_score"] == 88
    assert payload["analysis"]["recommendation"] == "Hire"
