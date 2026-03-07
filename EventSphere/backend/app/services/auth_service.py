from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database import supabase

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    # 🔐 Validate JWT with Supabase
    user_response = supabase.auth.get_user(token)

    if not user_response or not user_response.user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = user_response.user.id
    email = user_response.user.email

    # 🔎 Fetch role from profiles table (NOT users table anymore)
    profile_response = (
        supabase.table("profiles")
        .select("*")
        .eq("id", user_id)
        .single()
        .execute()
    )

    if not profile_response.data:
        raise HTTPException(status_code=404, detail="Profile not found")

    return {
        "id": user_id,
        "email": email,
        "role": profile_response.data["role"]
    }