from services.db_service import get_projects_collection, get_recommendations_collection


def get_dashboard_metrics():
    projects_col = get_projects_collection()
    rec_col = get_recommendations_collection()

    total_projects = projects_col.count_documents({})
    active_projects = projects_col.count_documents({"status": "active"})

    pipeline = [
        {"$group": {"_id": "$decision", "count": {"$sum": 1}}}
    ]
    decision_counts_raw = list(rec_col.aggregate(pipeline))
    decision_counts = {row["_id"]: row["count"] for row in decision_counts_raw}

    avg_budget_result = list(projects_col.aggregate([
        {"$group": {"_id": None, "avg_budget": {"$avg": "$budget"}}}
    ]))
    avg_budget = avg_budget_result[0]["avg_budget"] if avg_budget_result else 0

    return {
        "total_projects": total_projects,
        "active_projects": active_projects,
        "recommendation_distribution": decision_counts,
        "average_project_budget": round(float(avg_budget), 2) if avg_budget else 0,
    }
