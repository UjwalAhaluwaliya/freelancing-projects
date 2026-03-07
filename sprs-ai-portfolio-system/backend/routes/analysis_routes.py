from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from services.analysis_service import analyze_portfolio
from services.dashboard_service import get_dashboard_metrics
from services.recommendation_service import list_recommendations
from utils.auth_guard import ROLE_ADMIN, ROLE_PM, require_roles
from utils.responses import error_response, success_response
from utils.serializer import serialize_doc, serialize_docs

analysis_bp = Blueprint("analysis_bp", __name__)


@analysis_bp.post("/analyze_portfolio")
@require_roles(ROLE_ADMIN, ROLE_PM)
def analyze_portfolio_api():
    payload = request.get_json(silent=True) or {}
    analysis_name = payload.get("analysis_name")
    run_by_user_id = get_jwt_identity()

    analysis_doc, recommendations = analyze_portfolio(
        run_by_user_id=run_by_user_id,
        analysis_name=analysis_name,
    )

    if analysis_doc is None:
        return error_response("No projects found to analyze", status_code=400)

    return success_response(
        {
            "analysis": serialize_doc(analysis_doc),
            "recommendations": recommendations,
        },
        "Portfolio analyzed successfully",
        200,
    )


@analysis_bp.get("/recommendations")
@jwt_required()
def get_recommendations_api():
    analysis_id = request.args.get("analysis_id")
    docs = list_recommendations(analysis_id=analysis_id)
    return success_response(serialize_docs(docs), "Recommendations fetched")


@analysis_bp.get("/dashboard_metrics")
@jwt_required()
def dashboard_metrics_api():
    metrics = get_dashboard_metrics()
    return success_response(metrics, "Dashboard metrics fetched")
