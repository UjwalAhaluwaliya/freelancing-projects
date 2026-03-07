from datetime import datetime

from bson import ObjectId

from services.db_service import get_projects_collection, get_recommendations_collection


def ensure_indexes():
    col = get_recommendations_collection()
    col.create_index([("analysis_id", 1), ("project_id", 1)], unique=True)
    col.create_index([("decision", 1), ("created_at", -1)])


def save_recommendations(analysis_id: str, recommendations):
    col = get_recommendations_collection()
    now = datetime.utcnow()
    docs = []
    for rec in recommendations:
        doc = {
            "analysis_id": analysis_id,
            "project_id": rec["project_id"],
            "project_name": rec.get("project_name"),
            "decision": rec["decision"],
            "confidence_score": rec["confidence_score"],
            "priority_rank": rec["priority_rank"],
            "rationale": rec["rationale"],
            "created_at": now,
            "updated_at": now,
        }
        docs.append(doc)

    if docs:
        col.insert_many(docs, ordered=False)


def list_recommendations(analysis_id=None):
    col = get_recommendations_collection()
    projects_col = get_projects_collection()

    query = {}
    if analysis_id:
        query["analysis_id"] = analysis_id

    docs = list(col.find(query).sort("created_at", -1))

    missing_name_ids = []
    for doc in docs:
        if not doc.get("project_name") and doc.get("project_id"):
            missing_name_ids.append(doc["project_id"])

    if missing_name_ids:
        object_ids = []
        for pid in missing_name_ids:
            try:
                object_ids.append(ObjectId(pid))
            except Exception:
                continue

        if object_ids:
            name_map = {
                str(project["_id"]): project.get("project_name", "Unnamed Project")
                for project in projects_col.find({"_id": {"$in": object_ids}}, {"project_name": 1})
            }
            for doc in docs:
                if not doc.get("project_name"):
                    doc["project_name"] = name_map.get(doc.get("project_id"), "Unknown Project")

    return docs
