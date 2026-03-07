from app.services.ai_service import parse_resume_score_output


def test_parse_resume_score_output_from_json_block():
    raw = """
    ```json
    {
      "match_score": 82,
      "strengths": ["Python", "FastAPI"],
      "missing_skills": ["Kubernetes"],
      "recommendation": "Hire",
      "summary": "Strong backend fit"
    }
    ```
    """
    result = parse_resume_score_output(raw)

    assert result["match_score"] == 82
    assert result["recommendation"] == "Hire"
    assert result["strengths"] == ["Python", "FastAPI"]
    assert result["missing_skills"] == ["Kubernetes"]


def test_parse_resume_score_output_with_text_fallback():
    raw = "Candidate looks decent. Match Score: 74. Recommend: Consider."
    result = parse_resume_score_output(raw)

    assert result["match_score"] == 74
    assert result["recommendation"] == "Consider"
