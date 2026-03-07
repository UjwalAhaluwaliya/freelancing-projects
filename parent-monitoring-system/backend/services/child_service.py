from datetime import datetime
from typing import List, Optional

from bson import ObjectId

from ..database import get_collection
from ..models.child import Child, ChildCreate, ChildInDB
from .auth_service import AuthService

COLLECTION_NAME = "children"


class ChildService:
    """Service for child-related database operations."""

    @staticmethod
    async def get_by_id(child_id: str) -> Optional[ChildInDB]:
        """Get a child by ID with hashed password."""
        coll = get_collection(COLLECTION_NAME)
        try:
            doc = await coll.find_one({"_id": ObjectId(child_id)})
        except Exception:
            return None
        if not doc:
            return None
        doc["id"] = str(doc["_id"])
        doc["hashed_password"] = doc.pop("password", "")
        return ChildInDB(**doc)

    @staticmethod
    async def get_by_id_public(child_id: str) -> Optional[Child]:
        """Get a child by ID (without password)."""
        coll = get_collection(COLLECTION_NAME)
        try:
            doc = await coll.find_one({"_id": ObjectId(child_id)})
        except Exception:
            return None
        if not doc:
            return None
        doc["id"] = str(doc["_id"])
        doc.pop("password", None)
        return Child(**doc)

    @staticmethod
    async def get_by_name(name: str, parent_id: str | None = None) -> Optional[ChildInDB]:
        """Get child by name, optionally scoped to a parent."""
        coll = get_collection(COLLECTION_NAME)
        query = {"name": name}
        if parent_id:
            query["parent_id"] = parent_id
        doc = await coll.find_one(query)
        if not doc:
            return None
        doc["id"] = str(doc["_id"])
        doc["hashed_password"] = doc.pop("password", "")
        return ChildInDB(**doc)

    @staticmethod
    async def count_by_name(name: str) -> int:
        coll = get_collection(COLLECTION_NAME)
        return await coll.count_documents({"name": name})

    @staticmethod
    async def get_by_id_or_name(value: str, parent_id: str | None = None) -> Optional[ChildInDB]:
        """Get child by MongoDB ID OR by name (optionally parent-scoped)."""
        coll = get_collection(COLLECTION_NAME)

        if ObjectId.is_valid(value):
            query = {"_id": ObjectId(value)}
            if parent_id:
                query["parent_id"] = parent_id
            doc = await coll.find_one(query)
            if not doc:
                return None
            doc["id"] = str(doc["_id"])
            doc["hashed_password"] = doc.pop("password", "")
            return ChildInDB(**doc)

        return await ChildService.get_by_name(value, parent_id=parent_id)

    @staticmethod
    async def get_by_parent(parent_id: str) -> List[Child]:
        """Get all children for a parent."""
        coll = get_collection(COLLECTION_NAME)
        cursor = coll.find({"parent_id": parent_id})
        children = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            doc.pop("password", None)
            children.append(Child(**doc))
        return children

    @staticmethod
    async def create(child: ChildCreate, parent_id: str) -> Child:
        """Create a new child for a parent."""
        coll = get_collection(COLLECTION_NAME)
        hashed = AuthService.hash_password(child.password)
        now = datetime.utcnow()
        doc = {
            "parent_id": parent_id,
            "name": child.name,
            "age": child.age,
            "password": hashed,
            "created_at": now,
        }
        result = await coll.insert_one(doc)
        doc["_id"] = result.inserted_id
        doc["id"] = str(doc["_id"])
        doc.pop("password", None)
        return Child(**doc)
