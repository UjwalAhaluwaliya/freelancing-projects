from fastapi import APIRouter, HTTPException, Depends
from app.database import supabase
from app.schemas.profile_schema import ProfileCreate, ProfileAdminUpdate
from app.services.auth_dependency import admin_required
import uuid
from passlib.context import CryptContext

router = APIRouter(prefix="/profiles", tags=["Profiles"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ==========================
# CREATE PROFILE (ADMIN ONLY)
# ==========================
@router.post("/")
def create_profile(
    profile: ProfileCreate,
    user=Depends(admin_required)
):
    try:
        new_profile = {
            "id": str(uuid.uuid4()),
            "email": profile.email,
            "full_name": profile.full_name,
            "role": profile.role,
            "department": profile.department
        }

        response = supabase.table("profiles").insert(new_profile).execute()

        return {
            "success": True,
            "message": "Profile created successfully",
            "data": response.data
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# ==========================
# GET ALL PROFILES
# ==========================
@router.get("/")
def get_profiles(user=Depends(admin_required)):
    response = supabase.table("profiles").select("*").execute()

    return {
        "success": True,
        "data": response.data
    }


@router.put("/{profile_id}")
def update_profile(profile_id: str, payload: ProfileAdminUpdate, user=Depends(admin_required)):
    allowed_roles = {"admin", "hr", "employee"}
    update_data = {}

    if payload.full_name is not None:
        update_data["full_name"] = payload.full_name.strip()
    if payload.department is not None:
        update_data["department"] = payload.department.strip()
    if payload.role is not None:
        if payload.role not in allowed_roles:
            raise HTTPException(status_code=400, detail="Invalid role")
        update_data["role"] = payload.role
    if payload.password is not None:
        if len(payload.password) < 6:
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
        update_data["password"] = pwd_context.hash(payload.password)

    if not update_data:
        raise HTTPException(status_code=400, detail="No update fields provided")

    try:
        update_response = (
            supabase.table("profiles")
            .update(update_data)
            .eq("id", profile_id)
            .execute()
        )
        # If update affected no rows, surface a clear error instead of silent success.
        if hasattr(update_response, "data") and update_response.data == []:
            raise HTTPException(
                status_code=409,
                detail=(
                    "Profile update did not persist. Check profile_id, Supabase project, "
                    "and table RLS/policies for UPDATE."
                ),
            )

        refreshed = (
            supabase.table("profiles")
            .select("*")
            .eq("id", profile_id)
            .execute()
        )
        if not refreshed.data:
            raise HTTPException(status_code=404, detail="Profile not found")

        current = refreshed.data[0]
        for key, expected in update_data.items():
            if key not in current:
                continue
            if key == "password":
                # Password is hashed, only require that it exists.
                if not current.get("password"):
                    raise HTTPException(
                        status_code=409,
                        detail="Password update did not persist. Check Supabase UPDATE policy.",
                    )
            else:
                if str(current.get(key, "")) != str(expected):
                    raise HTTPException(
                        status_code=409,
                        detail=(
                            f"Field '{key}' did not persist. Check Supabase UPDATE policy "
                            "or confirm you're connected to the correct project."
                        ),
                    )
        return {
            "success": True,
            "message": "User updated successfully",
            "data": refreshed.data,
        }
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
