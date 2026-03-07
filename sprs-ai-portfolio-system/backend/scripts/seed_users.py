from __future__ import annotations

import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app import create_app
from services.db_service import get_users_collection
from services.user_service import create_user


DEFAULT_USERS = [
    {
        "full_name": "System Admin",
        "email": "admin@sprs.local",
        "password": "admin123",
        "role": "admin",
    },
    {
        "full_name": "Portfolio Manager",
        "email": "pm@sprs.local",
        "password": "pm123",
        "role": "project_manager",
    },
    {
        "full_name": "Business Employee",
        "email": "employee@sprs.local",
        "password": "employee123",
        "role": "employee",
    },
]


def main() -> None:
    load_dotenv()
    app = create_app()
    with app.app_context():
        users = get_users_collection()
        for entry in DEFAULT_USERS:
            existing = users.find_one({"email": entry["email"]})
            if existing:
                print(f"Exists: {entry['email']}")
                continue
            create_user(
                full_name=entry["full_name"],
                email=entry["email"],
                password=entry["password"],
                role=entry["role"],
            )
            print(f"Created: {entry['email']} ({entry['role']})")


if __name__ == "__main__":
    main()
