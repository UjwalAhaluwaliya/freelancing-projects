from app.database import supabase

def create_notification(user_id: str, title: str, message: str):
    try:
        print("🔔 Creating notification for:", user_id)

        response = supabase.table("notifications").insert({
            "user_id": user_id,
            "title": title,
            "message": message
        }).execute()

        print("🔔 Insert response:", response.data)

    except Exception as e:
        print("❌ Notification Error:", e)