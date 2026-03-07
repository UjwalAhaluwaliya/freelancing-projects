from fastapi import APIRouter, Depends, HTTPException
from app.schemas.event_schema import EventCreate
from app.database import supabase
from app.services.auth_service import verify_token
from app.schemas.registration_schema import RegistrationCreate
from app.schemas.judge_schema import AssignJudge
from app.schemas.score_schema import ScoreCreate
from app.schemas.criteria_schema import CriteriaCreate
from app.schemas.event_criteria_schema import EventCriteriaCreate

router = APIRouter()


@router.post("/events")
def create_event(event: EventCreate, user=Depends(verify_token)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create event")

    response = supabase.table("events").insert({
        "title": event.title,
        "description": event.description,
        "category": event.category,
        "max_participants": event.max_participants,
        "registration_deadline": str(event.registration_deadline),
        "created_by": user["id"]
    }).execute()

    return response.data


@router.get("/events")
def get_events():
    response = supabase.table("events").select("*").execute()
    return response.data


@router.post("/register")
def register_for_event(registration: RegistrationCreate, user=Depends(verify_token)):
    if user["role"] != "participant":
        raise HTTPException(status_code=403, detail="Only participants can register")

    # Check duplicate registration
    existing = supabase.table("registrations") \
        .select("*") \
        .eq("event_id", registration.event_id) \
        .eq("participant_id", user["id"]) \
        .execute()

    if existing.data:
        raise HTTPException(status_code=409, detail="Already registered for this event")

    response = supabase.table("registrations").insert({
        "event_id": registration.event_id,
        "participant_id": user["id"]
    }).execute()

    return response.data


@router.post("/assign-judge")
def assign_judge(data: AssignJudge, user=Depends(verify_token)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin can assign judges")

    response = supabase.table("event_judges").insert({
        "event_id": data.event_id,
        "judge_id": data.judge_id
    }).execute()

    return response.data


@router.post("/submit-score")
def submit_score(data: ScoreCreate, user=Depends(verify_token)):
    if user["role"] != "judge":
        raise HTTPException(status_code=403, detail="Only judges can submit scores")

    # Check if judge assigned to event
    assignment = supabase.table("event_judges") \
        .select("*") \
        .eq("event_id", data.event_id) \
        .eq("judge_id", user["id"]) \
        .execute()

    if not assignment.data:
        raise HTTPException(status_code=403, detail="You are not assigned to this event")

    existing_score = supabase.table("scores") \
        .select("*") \
        .eq("event_id", data.event_id) \
        .eq("participant_id", data.participant_id) \
        .eq("judge_id", user["id"]) \
        .eq("criteria_id", data.criteria_id) \
        .execute()

    if existing_score.data:
        raise HTTPException(status_code=409, detail="Score already submitted for this participant")

    response = supabase.table("scores").insert({
        "event_id": data.event_id,
        "participant_id": data.participant_id,
        "judge_id": user["id"],
        "criteria_id": data.criteria_id,
        "score": data.score
    }).execute()

    return response.data


@router.post("/create-criteria")
def create_criteria(data: CriteriaCreate, user=Depends(verify_token)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create criteria")

    response = supabase.table("criteria").insert({
        "title": data.title,
        "description": data.description
    }).execute()

    return response.data


@router.post("/map-criteria")
def map_criteria(data: EventCriteriaCreate, user=Depends(verify_token)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin can map criteria")

    # Check duplicate mapping
    existing = supabase.table("event_criteria") \
        .select("*") \
        .eq("event_id", data.event_id) \
        .eq("criteria_id", data.criteria_id) \
        .execute()

    if existing.data:
        raise HTTPException(status_code=409, detail="Criteria already mapped to this event")

    response = supabase.table("event_criteria").insert({
        "event_id": data.event_id,
        "criteria_id": data.criteria_id,
        "weight": data.weight
    }).execute()

    return response.data


@router.get("/my-result/{event_id}")
def my_result(event_id: str, user=Depends(verify_token)):
    role = user["role"]
    user_id = user["id"]

    # Get weights
    criteria_weights = supabase.table("event_criteria") \
        .select("*") \
        .eq("event_id", event_id) \
        .execute()

    weight_map = {c["criteria_id"]: c["weight"] for c in criteria_weights.data}

    if role == "judge":
        scores = supabase.table("scores") \
            .select("*") \
            .eq("event_id", event_id) \
            .eq("judge_id", user_id) \
            .execute()

    elif role == "participant":
        scores = supabase.table("scores") \
            .select("*") \
            .eq("event_id", event_id) \
            .execute()

    else:
        raise HTTPException(status_code=403, detail="Invalid role")

    if not scores.data:
        return {"message": "No scores found"}

    participant_scores = {}

    for s in scores.data:
        pid = s["participant_id"]
        cid = s["criteria_id"]
        score = s["score"]
        weight = weight_map.get(cid, 0)

        weighted = score * weight

        if pid not in participant_scores:
            participant_scores[pid] = 0

        participant_scores[pid] += weighted

    sorted_results = sorted(
        participant_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    ranked = []
    rank = 1

    for pid, total in sorted_results:
        ranked.append({
            "participant_id": pid,
            "total_score": round(total, 2),
            "rank": rank
        })
        rank += 1

    if role == "participant":
        for r in ranked:
            if r["participant_id"] == user_id:
                return r
        return {"message": "You did not participate"}

    return ranked


@router.get("/my-scored-events")
def my_scored_events(user=Depends(verify_token)):
    if user["role"] != "participant":
        raise HTTPException(status_code=403, detail="Only participants can access this")

    scores = supabase.table("scores") \
        .select("event_id") \
        .eq("participant_id", user["id"]) \
        .execute()

    event_ids = sorted({row["event_id"] for row in scores.data}) if scores.data else []
    return {"event_ids": event_ids}


@router.put("/publish-result/{event_id}")
def publish_result(event_id: str, user=Depends(verify_token)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin can publish result")

    response = supabase.table("events") \
        .update({"is_published": True}) \
        .eq("id", event_id) \
        .execute()

    return {"message": "Result published successfully"}


@router.get("/me")
def get_me(user=Depends(verify_token)):
    return {
        "id": user["id"],
        "email": user["email"],
        "role": user["role"]
    }


@router.get("/criteria")
def get_criteria():
    response = supabase.table("criteria").select("*").execute()
    return response.data


@router.put("/change-role")
def change_role(user_id: str, role: str, user=Depends(verify_token)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin can change roles")

    supabase.table("profiles") \
        .update({"role": role}) \
        .eq("id", user_id) \
        .execute()

    return {"message": "Role updated successfully"}


@router.get("/my-events")
def my_events(user=Depends(verify_token)):
    if user["role"] != "judge":
        raise HTTPException(status_code=403, detail="Only judges can access this")

    # Get event IDs assigned to this judge
    assignments = supabase.table("event_judges") \
        .select("event_id") \
        .eq("judge_id", user["id"]) \
        .execute()

    if not assignments.data:
        return []

    event_ids = [a["event_id"] for a in assignments.data]

    # Fetch event details for those IDs
    events = supabase.table("events") \
        .select("*") \
        .in_("id", event_ids) \
        .execute()

    return events.data


@router.get("/event-criteria/{event_id}")
def get_event_criteria(event_id: str):
    # Get criteria IDs and weights mapped to this event
    mappings = supabase.table("event_criteria") \
        .select("criteria_id, weight") \
        .eq("event_id", event_id) \
        .execute()

    if not mappings.data:
        return []

    criteria_ids = [m["criteria_id"] for m in mappings.data]
    weight_map = {m["criteria_id"]: m["weight"] for m in mappings.data}

    # Fetch criteria details
    criteria = supabase.table("criteria") \
        .select("*") \
        .in_("id", criteria_ids) \
        .execute()

    # Attach weight to each criteria
    result = []
    for c in criteria.data:
        result.append({
            **c,
            "weight": weight_map.get(c["id"], 0)
        })

    return result


@router.get("/my-registrations")
def my_registrations(user=Depends(verify_token)):
    response = supabase.table("registrations") \
        .select("*") \
        .eq("participant_id", user["id"]) \
        .execute()

    return response.data
