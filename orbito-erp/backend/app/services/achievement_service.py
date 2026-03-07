from app.database import supabase

def add_points(user_id: str, points: int, reason: str):
    try:
        response = supabase.table("achievements").insert({
            "user_id": user_id,
            "points": points,
            "reason": reason
        }).execute()

        print(f"🏆 Points added: {points} to {user_id}")

        return response.data

    except Exception as e:
        print("Achievement Error:", e)