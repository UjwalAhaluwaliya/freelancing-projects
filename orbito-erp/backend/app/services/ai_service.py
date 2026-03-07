import json
import re
from io import BytesIO
from typing import Any, Dict, List
from google import genai
from google.genai import errors as genai_errors
from pypdf import PdfReader
from app.core.config import settings

client = genai.Client(api_key=settings.gemini_api_key)
MODEL_FALLBACKS = [
    settings.gemini_model,
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
]


class AIQuotaExceededError(Exception):
    pass


def _is_quota_error(exc: Exception) -> bool:
    message = str(exc).lower()
    return "resource_exhausted" in message or "quota" in message or "429" in message


def _generate_text(prompt: str) -> str:
    last_error = None
    seen = set()
    for model_name in MODEL_FALLBACKS:
        if not model_name or model_name in seen:
            continue
        seen.add(model_name)
        try:
            response = client.models.generate_content(model=model_name, contents=prompt)
            return (response.text or "").strip()
        except genai_errors.ClientError as exc:
            last_error = exc
            if _is_quota_error(exc):
                raise AIQuotaExceededError(str(exc)) from exc
            message = str(exc)
            if "NOT_FOUND" in message or "not found" in message.lower():
                continue
            raise
    if last_error:
        raise RuntimeError(f"Gemini model error: {last_error}") from last_error
    raise RuntimeError("No valid Gemini model configured")


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(pdf_bytes))
    page_texts = [(page.extract_text() or "").strip() for page in reader.pages]
    text = "\n".join(chunk for chunk in page_texts if chunk)
    return text.strip()


def _extract_json_from_text(text: str) -> Dict[str, Any]:
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL | re.IGNORECASE)
    if fenced:
        try:
            return json.loads(fenced.group(1))
        except json.JSONDecodeError:
            pass

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass

    return {}


def _as_string_list(value: Any) -> List[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        items = [part.strip() for part in value.split(",")]
        return [item for item in items if item]
    return []


def _keywords(text: str) -> List[str]:
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9+#.-]{2,}", text.lower())
    stop = {
        "the",
        "and",
        "for",
        "with",
        "that",
        "from",
        "this",
        "are",
        "you",
        "your",
        "will",
        "have",
        "job",
        "resume",
        "description",
        "experience",
        "required",
        "candidate",
        "role",
    }
    return [w for w in words if w not in stop]


def parse_resume_score_output(text: str) -> Dict[str, Any]:
    parsed = _extract_json_from_text(text)

    match_score = parsed.get("match_score")
    if match_score is None:
        score_match = re.search(r"match\s*score[^0-9]*([0-9]{1,3})", text, re.IGNORECASE)
        match_score = int(score_match.group(1)) if score_match else 0

    try:
        match_score = int(float(match_score))
    except (TypeError, ValueError):
        match_score = 0

    match_score = max(0, min(100, match_score))
    strengths = _as_string_list(parsed.get("strengths", []))
    missing_skills = _as_string_list(parsed.get("missing_skills", []))
    recommendation = str(parsed.get("recommendation", "Consider")).strip() or "Consider"
    summary = str(parsed.get("summary", "")).strip()

    return {
        "match_score": match_score,
        "strengths": strengths,
        "missing_skills": missing_skills,
        "recommendation": recommendation,
        "summary": summary,
        "raw_output": text,
    }


def generate_job_description_local(
    title: str, skills: str, experience: str, department: str
) -> str:
    skill_items = [s.strip() for s in skills.split(",") if s.strip()]
    skills_block = "\n".join([f"- {item}" for item in skill_items[:8]]) or "- Domain knowledge"
    return (
        f"Job Title: {title}\n"
        f"Department: {department}\n\n"
        "Job Summary:\n"
        f"We are hiring a {title} to strengthen our {department} team.\n\n"
        "Key Responsibilities:\n"
        "- Build and maintain high-quality deliverables.\n"
        "- Collaborate with HR and stakeholders.\n"
        "- Follow process, timelines, and reporting standards.\n"
        "- Contribute to continuous improvement initiatives.\n"
        "- Support cross-functional execution.\n\n"
        "Required Qualifications:\n"
        f"- {experience} experience in relevant role.\n"
        f"{skills_block}\n\n"
        "Preferred Qualifications:\n"
        "- Strong communication and ownership mindset.\n"
        "- Ability to work in collaborative teams.\n\n"
        "Benefits:\n"
        "- Learning opportunities\n"
        "- Growth-focused culture\n"
        "- Flexible working support\n"
    )


def score_resume_local(resume_text: str, job_description: str) -> Dict[str, Any]:
    jd = _keywords(job_description)
    cv = set(_keywords(resume_text))
    jd_unique = []
    seen = set()
    for token in jd:
        if token not in seen:
            jd_unique.append(token)
            seen.add(token)

    overlap = [token for token in jd_unique if token in cv]
    missing = [token for token in jd_unique if token not in cv]
    ratio = (len(overlap) / max(1, len(jd_unique)))
    score = max(35, min(95, int(35 + ratio * 65)))

    if score >= 75:
        rec = "Hire"
    elif score >= 55:
        rec = "Consider"
    else:
        rec = "Reject"

    return {
        "match_score": score,
        "strengths": overlap[:6],
        "missing_skills": missing[:6],
        "recommendation": rec,
        "summary": f"Heuristic fallback score based on skill overlap ({len(overlap)} matched).",
        "raw_output": "local-fallback",
    }


def policy_chatbot_local(question: str) -> str:
    q = question.lower()
    if "casual" in q or "leave" in q:
        return "Employees get 12 casual leaves per year. Leave requests require manager approval."
    if "sick" in q:
        return "Sick leave is allowed with valid medical proof as per policy."
    if "notice" in q:
        return "Standard notice period is 60 days."
    if "wfh" in q or "work from home" in q:
        return "Work from home is allowed up to 2 days per week, based on manager approval."
    if "review" in q or "performance" in q:
        return "Performance reviews are scheduled every 6 months."
    return (
        "As per Orbito policy, approvals depend on reporting manager and HR process. "
        "Please share your exact case for detailed guidance."
    )


async def generate_job_description(title: str, skills: str, experience: str, department: str) -> str:
    prompt = f"""
You are an expert HR recruiter.
Create a production-ready job description.

Job Title: {title}
Department: {department}
Required Skills: {skills}
Experience: {experience}

Output sections:
1) Job Summary
2) Key Responsibilities (5-7 points)
3) Required Qualifications
4) Preferred Qualifications
5) Benefits
"""
    return _generate_text(prompt)


async def score_resume(resume_text: str, job_description: str) -> Dict[str, Any]:
    prompt = f"""
You are an HR screening assistant.
Compare the resume with the job description.
Return only strict JSON with this schema:
{{
  "match_score": 0-100,
  "strengths": ["..."],
  "missing_skills": ["..."],
  "recommendation": "Hire|Consider|Reject",
  "summary": "short summary"
}}

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}
"""
    raw_text = _generate_text(prompt)
    return parse_resume_score_output(raw_text)


async def policy_chatbot(question: str) -> str:
    prompt = f"""
You are the HR assistant of Orbito Company.

Company Policies:
- Employees get 12 casual leaves per year.
- Sick leave allowed with medical proof.
- Notice period is 60 days.
- Work from home allowed twice per week.
- Leave approval depends on manager decision.
- Performance review happens every 6 months.

Answer clearly and professionally.

Question:
{question}
"""
    return _generate_text(prompt)
