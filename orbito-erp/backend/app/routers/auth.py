from fastapi import APIRouter, HTTPException
from app.database import supabase
from app.services.jwt_service import (
    create_access_token,
    create_refresh_token,
    verify_token
)
from passlib.context import CryptContext

router = APIRouter(prefix="/auth", tags=["Authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ==========================
# REGISTER
# ==========================
@router.post("/register")
def register(email: str, password: str, full_name: str, role: str):
    allowed_roles = {"admin", "hr", "employee"}
    if role not in allowed_roles:
        raise HTTPException(status_code=400, detail="Invalid role")

    # Check if user already exists
    existing_user = supabase.table("profiles") \
        .select("*") \
        .eq("email", email) \
        .execute()

    if existing_user.data:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = pwd_context.hash(password)

    response = supabase.table("profiles").insert({
        "email": email,
        "full_name": full_name,
        "role": role,
        "password": hashed_password
    }).execute()

    return {
        "success": True,
        "message": "User registered successfully",
        "data": response.data
    }


# ==========================
# LOGIN
# ==========================
@router.post("/login")
def login(email: str, password: str):

    user = supabase.table("profiles") \
        .select("*") \
        .eq("email", email) \
        .execute()

    if not user.data:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_data = user.data[0]
    stored_password = user_data.get("password")
    if not stored_password:
        raise HTTPException(
            status_code=401,
            detail="Account password is not set yet. Ask admin to reset password.",
        )

    if not pwd_context.verify(password, stored_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({
        "user_id": user_data["id"],
        "role": user_data["role"]
    })

    refresh_token = create_refresh_token({
        "user_id": user_data["id"],
        "role": user_data["role"]
    })

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# ==========================
# REFRESH ACCESS TOKEN
# ==========================
@router.post("/refresh")
def refresh(refresh_token: str):

    payload = verify_token(refresh_token)

    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = create_access_token({
        "user_id": payload["user_id"],
        "role": payload["role"]
    })

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }
