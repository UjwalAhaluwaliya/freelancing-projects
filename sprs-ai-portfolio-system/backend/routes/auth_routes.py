from flask import Blueprint, request
from flask_jwt_extended import create_access_token

from services.user_service import validate_credentials
from utils.responses import error_response, success_response

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.post("/auth/login")
def login():
    payload = request.get_json(silent=True) or {}
    email = str(payload.get("email", "")).strip()
    password = str(payload.get("password", "")).strip()

    if not email or not password:
        return error_response("Email and password are required", status_code=400)

    user = validate_credentials(email, password)
    if not user:
        return error_response("Invalid credentials", status_code=401)

    token = create_access_token(
        identity=str(user["_id"]),
        additional_claims={"role": user.get("role", "employee"), "email": user.get("email", "")},
    )

    return success_response(
        {
            "access_token": token,
            "user": {
                "id": str(user["_id"]),
                "full_name": user.get("full_name"),
                "email": user.get("email"),
                "role": user.get("role"),
            },
        },
        "Login successful",
    )
