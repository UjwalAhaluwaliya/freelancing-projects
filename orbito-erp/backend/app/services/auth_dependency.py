from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.jwt_service import verify_token

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload


def hr_or_admin_required(user=Depends(get_current_user)):
    if user["role"] not in ["hr", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    return user


def employee_required(user=Depends(get_current_user)):
    if user["role"] != "employee":
        raise HTTPException(status_code=403, detail="Access denied")
    return user

def admin_required(user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user