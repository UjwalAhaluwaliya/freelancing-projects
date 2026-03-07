from bson import ObjectId
from pymongo import DESCENDING

from services.db_service import get_projects_collection


def ensure_indexes():
    col = get_projects_collection()
    col.create_index([("project_name", 1)])
    col.create_index([("status", 1), ("updated_at", DESCENDING)])


def add_project(project_doc):
    col = get_projects_collection()
    result = col.insert_one(project_doc)
    return str(result.inserted_id)


def list_projects(filters=None):
    col = get_projects_collection()
    filters = filters or {}
    return list(col.find(filters).sort("updated_at", DESCENDING))


def get_project_by_id(project_id: str):
    col = get_projects_collection()
    return col.find_one({"_id": ObjectId(project_id)})


def delete_project_by_id(project_id: str):
    col = get_projects_collection()
    result = col.delete_one({"_id": ObjectId(project_id)})
    return result.deleted_count
