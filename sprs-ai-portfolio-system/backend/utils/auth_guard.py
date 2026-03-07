from functools import wraps

from flask_jwt_extended import get_jwt, verify_jwt_in_request

from utils.responses import error_response


ROLE_ADMIN = "admin"
ROLE_PM = "project_manager"
ROLE_EMPLOYEE = "employee"


def require_roles(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get("role")
            if user_role not in allowed_roles:
                return error_response("Forbidden: insufficient permissions", status_code=403)
            return fn(*args, **kwargs)

        return wrapper

    return decorator
