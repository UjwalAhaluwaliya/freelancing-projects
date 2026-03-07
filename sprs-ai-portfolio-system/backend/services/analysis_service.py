from datetime import datetime

from services.db_service import get_portfolio_analysis_collection
from services.project_service import list_projects
from services.recommendation_service import save_recommendations
from ml_models.pipeline import run_analysis


def ensure_indexes():
    col = get_portfolio_analysis_collection()
    col.create_index([("created_at", -1)])
    col.create_index([("analysis_status", 1), ("created_at", -1)])


def analyze_portfolio(run_by_user_id=None, analysis_name=None):
    projects = list_projects()
    if not projects:
        return None, []

    now = datetime.utcnow()
    analysis_doc = {
        "analysis_name": analysis_name or f"Analysis {now.strftime('%Y-%m-%d %H:%M:%S')}",
        "run_by_user_id": run_by_user_id,
        "analysis_status": "running",
        "project_ids": [str(p["_id"]) for p in projects],
        "created_at": now,
        "started_at": now,
    }

    col = get_portfolio_analysis_collection()
    insert_result = col.insert_one(analysis_doc)
    analysis_id = str(insert_result.inserted_id)

    analysis_payload, recommendations = run_analysis(projects)

    col.update_one(
        {"_id": insert_result.inserted_id},
        {
            "$set": {
                "analysis_status": "completed",
                "model_outputs": analysis_payload.get("model_outputs", {}),
                "summary": analysis_payload.get("summary", {}),
                "completed_at": datetime.utcnow(),
            }
        },
    )

    save_recommendations(analysis_id, recommendations)

    final_doc = col.find_one({"_id": insert_result.inserted_id})
    return final_doc, recommendations
