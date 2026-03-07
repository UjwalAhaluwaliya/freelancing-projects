from datetime import datetime
from typing import Optional

from bson import ObjectId

from ..database import get_collection
from ..models.parent import Parent, ParentCreate, ParentInDB, ParentProfileUpdate
from .auth_service import AuthService

COLLECTION_NAME = "parents"


class ParentService:
    """Service for parent-related database operations."""

    @staticmethod
    def _serialize_doc(doc: dict) -> dict:
        """Convert MongoDB document to API-friendly format."""
        doc["id"] = str(doc.pop("_id", ""))
        return doc

    @staticmethod
    async def get_by_email(email: str) -> Optional[ParentInDB]:
        """Get a parent by email."""
        coll = get_collection(COLLECTION_NAME)
        doc = await coll.find_one({"email": email.lower()})
        if not doc:
            return None
        doc["id"] = str(doc["_id"])
        doc["hashed_password"] = doc.pop("password")
        return ParentInDB(**doc)

    @staticmethod
    async def get_by_id(parent_id: str) -> Optional[Parent]:
        """Get a parent by ID."""
        coll = get_collection(COLLECTION_NAME)
        try:
            doc = await coll.find_one({"_id": ObjectId(parent_id)})
        except Exception:
            return None
        if not doc:
            return None
        doc["id"] = str(doc["_id"])
        doc.pop("password", None)
        return Parent(**doc)

    @staticmethod
    async def create(parent: ParentCreate) -> Parent:
        """Create a new parent."""
        coll = get_collection(COLLECTION_NAME)
        hashed = AuthService.hash_password(parent.password)
        now = datetime.utcnow()
        doc = {
            "name": parent.name,
            "email": parent.email.lower(),
            "password": hashed,
            "phone": None,
            "created_at": now,
        }
        result = await coll.insert_one(doc)
        doc["_id"] = result.inserted_id
        doc["id"] = str(doc["_id"])
        doc.pop("password", None)
        return Parent(**doc)

    @staticmethod
    async def reset_password_by_email(email: str, new_password: str) -> bool:
        """Reset parent password by email. Returns True if updated."""
        coll = get_collection(COLLECTION_NAME)
        hashed = AuthService.hash_password(new_password)
        result = await coll.update_one(
            {"email": email.lower()},
            {
                "$set": {
                    "password": hashed,
                    "updated_at": datetime.utcnow(),
                }
            },
        )
        return result.matched_count > 0

    @staticmethod
    async def update_profile(parent_id: str, body: ParentProfileUpdate) -> Optional[Parent]:
        coll = get_collection(COLLECTION_NAME)
        updates: dict = {}

        if body.name is not None:
            updates["name"] = body.name.strip()
        if body.email is not None:
            updates["email"] = body.email.lower()
        if body.phone is not None:
            updates["phone"] = body.phone.strip()

        if not updates:
            return await ParentService.get_by_id(parent_id)

        updates["updated_at"] = datetime.utcnow()

        try:
            await coll.update_one(
                {"_id": ObjectId(parent_id)},
                {"$set": updates},
            )
        except Exception:
            return None

        return await ParentService.get_by_id(parent_id)
