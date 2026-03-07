from bson.errors import InvalidId
from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from services.project_service import (
    add_project,
    delete_project_by_id,
    get_project_by_id,
    list_projects,
)
from utils.auth_guard import ROLE_ADMIN, ROLE_PM, require_roles
from utils.responses import error_response, success_response
from utils.serializer import serialize_doc, serialize_docs
from utils.validators import normalize_project_payload, validate_project_payload

project_bp = Blueprint("project_bp", __name__)


@project_bp.post("/add_project")
@require_roles(ROLE_ADMIN, ROLE_PM)
def create_project():
    payload = request.get_json(silent=True)
    errors = validate_project_payload(payload)
    if errors:
        return error_response("Validation failed", errors=errors, status_code=400)

    doc = normalize_project_payload(payload)
    inserted_id = add_project(doc)
    return success_response({"project_id": inserted_id}, "Project added successfully", 201)


@project_bp.get("/projects")
@jwt_required()
def get_projects():
    status = request.args.get("status")
    query = {"status": status.lower()} if status else {}
    docs = list_projects(query)
    return success_response(serialize_docs(docs), "Projects fetched")


@project_bp.get("/project/<project_id>")
@jwt_required()
def get_project(project_id):
    try:
        doc = get_project_by_id(project_id)
    except InvalidId:
        return error_response("Invalid project id", status_code=400)

    if not doc:
        return error_response("Project not found", status_code=404)

    return success_response(serialize_doc(doc), "Project fetched")


@project_bp.delete("/project/<project_id>")
@require_roles(ROLE_ADMIN, ROLE_PM)
def delete_project(project_id):
    try:
        deleted_count = delete_project_by_id(project_id)
    except InvalidId:
        return error_response("Invalid project id", status_code=400)

    if deleted_count == 0:
        return error_response("Project not found", status_code=404)

    return success_response(message="Project deleted")
