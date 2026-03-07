from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from services.db_service import get_users_collection


ALLOWED_ROLES = {"admin", "project_manager", "employee"}


def ensure_indexes():
    col = get_users_collection()
    col.create_index("email", unique=True)
    col.create_index("role")


def create_user(full_name: str, email: str, password: str, role: str):
    col = get_users_collection()
    role = role.strip().lower()
    if role not in ALLOWED_ROLES:
        raise ValueError("Invalid role")

    now = datetime.utcnow()
    user = {
        "full_name": full_name.strip(),
        "email": email.strip().lower(),
        "password_hash": generate_password_hash(password),
        "role": role,
        "status": "active",
        "created_at": now,
        "updated_at": now,
    }
    result = col.insert_one(user)
    user["_id"] = result.inserted_id
    return user


def get_user_by_email(email: str):
    col = get_users_collection()
    return col.find_one({"email": email.strip().lower()})


def validate_credentials(email: str, password: str):
    user = get_user_by_email(email)
    if not user:
        return None
    if user.get("status") != "active":
        return None
    if not check_password_hash(user.get("password_hash", ""), password):
        return None
    return user
