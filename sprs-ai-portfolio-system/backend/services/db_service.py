from pymongo import MongoClient

_client = None
_db = None


def init_db(app):
    global _client, _db
    _client = MongoClient(app.config["MONGO_URI"])
    _db = _client[app.config["MONGO_DB_NAME"]]


def get_db():
    if _db is None:
        raise RuntimeError("Database not initialized. Call init_db first.")
    return _db


def get_projects_collection():
    return get_db()["projects"]


def get_recommendations_collection():
    return get_db()["recommendations"]


def get_portfolio_analysis_collection():
    return get_db()["portfolio_analysis"]


def get_users_collection():
    return get_db()["users"]
