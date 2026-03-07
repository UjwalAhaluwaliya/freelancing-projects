from __future__ import annotations

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()


def main() -> None:
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    db_name = os.getenv("MONGO_DB_NAME", "sprs_db")

    sample_path = Path(__file__).resolve().parents[1] / "ml_models" / "sample_projects.json"
    data = json.loads(sample_path.read_text(encoding="utf-8"))

    client = MongoClient(mongo_uri)
    db = client[db_name]
    projects_col = db["projects"]

    projects_col.delete_many({})
    if data:
        projects_col.insert_many(data)

    print(f"Seeded {len(data)} projects into {db_name}.projects")


if __name__ == "__main__":
    main()
