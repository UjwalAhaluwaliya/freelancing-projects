from fastapi import APIRouter, HTTPException
from app.database import supabase

router = APIRouter(prefix="/achievements", tags=["Achievements"])


# ==========================
# GET TOTAL POINTS OF USER
# ==========================
@router.get("/total/{user_id}")
def get_total_points(user_id: str):
    try:
        response = supabase.table("achievements") \
            .select("points") \
            .eq("user_id", user_id) \
            .execute()

        if not response.data:
            return {
                "success": True,
                "user_id": user_id,
                "total_points": 0
            }

        total = sum(item["points"] for item in response.data)

        return {
            "success": True,
            "user_id": user_id,
            "total_points": total
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==========================
# LEADERBOARD (TOP USERS)
# ==========================
@router.get("/leaderboard")
def leaderboard():
    try:
        response = supabase.table("achievements") \
            .select("user_id, points") \
            .execute()

        if not response.data:
            return {
                "success": True,
                "leaderboard": []
            }

        # Aggregate points per user
        user_points = {}

        for row in response.data:
            user_id = row["user_id"]
            points = row["points"]

            if user_id not in user_points:
                user_points[user_id] = 0

            user_points[user_id] += points

        # Convert to sorted list
        leaderboard = sorted(
            user_points.items(),
            key=lambda x: x[1],
            reverse=True
        )

        # Fetch profile names
        result = []

        for user_id, total_points in leaderboard:

            profile = supabase.table("profiles") \
                .select("full_name") \
                .eq("id", user_id) \
                .execute()

            name = profile.data[0]["full_name"] if profile.data else "Unknown"

            result.append({
                "user_id": user_id,
                "full_name": name,
                "total_points": total_points
            })

        return {
            "success": True,
            "leaderboard": result
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))