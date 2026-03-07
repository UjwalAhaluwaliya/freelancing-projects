from datetime import datetime

REQUIRED_FIELDS = {
    "project_name": str,
    "description": str,
    "budget": (int, float),
    "expected_roi": (int, float),
    "risk_level": str,
    "team_size": int,
    "technology_stack": list,
    "duration": (int, float),
    "strategic_alignment_score": (int, float),
    "status": str,
}

ALLOWED_RISK_LEVELS = {"low", "medium", "high"}
ALLOWED_STATUSES = {"proposed", "active", "on_hold", "completed", "retired"}


def validate_project_payload(payload):
    errors = []

    if not isinstance(payload, dict):
        return ["Payload must be a JSON object."]

    for key, expected_type in REQUIRED_FIELDS.items():
        if key not in payload:
            errors.append(f"Missing required field: {key}")
            continue
        if not isinstance(payload[key], expected_type):
            errors.append(f"Invalid type for {key}")

    risk_level = str(payload.get("risk_level", "")).lower()
    if risk_level and risk_level not in ALLOWED_RISK_LEVELS:
        errors.append("risk_level must be one of: low, medium, high")

    status = str(payload.get("status", "")).lower()
    if status and status not in ALLOWED_STATUSES:
        errors.append("status must be one of: proposed, active, on_hold, completed, retired")

    tech_stack = payload.get("technology_stack", [])
    if isinstance(tech_stack, list) and any(not isinstance(item, str) for item in tech_stack):
        errors.append("technology_stack must be an array of strings")

    return errors


def normalize_project_payload(payload):
    now = datetime.utcnow()
    return {
        "project_name": payload["project_name"].strip(),
        "description": payload["description"].strip(),
        "budget": float(payload["budget"]),
        "expected_roi": float(payload["expected_roi"]),
        "risk_level": payload["risk_level"].lower(),
        "team_size": int(payload["team_size"]),
        "technology_stack": payload["technology_stack"],
        "duration": float(payload["duration"]),
        "strategic_alignment_score": float(payload["strategic_alignment_score"]),
        "status": payload["status"].lower(),
        "created_at": now,
        "updated_at": now,
    }
