from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure

from .config import settings

# MongoDB client instance
client: AsyncIOMotorClient | None = None


async def connect_to_mongodb() -> AsyncIOMotorClient:
    """Establish connection to MongoDB."""
    global client
    client = AsyncIOMotorClient(
        settings.mongodb_url,
        serverSelectionTimeoutMS=5000,
    )
    try:
        await client.admin.command("ping")
    except ConnectionFailure as e:
        raise ConnectionFailure(f"Failed to connect to MongoDB: {e}") from e
    return client


async def close_mongodb_connection() -> None:
    """Close MongoDB connection."""
    global client
    if client:
        client.close()
        client = None


def get_database():
    """Get database instance. Raises if not connected."""
    if client is None:
        raise RuntimeError("MongoDB client not initialized. Call connect_to_mongodb first.")
    return client[settings.database_name]


def get_collection(collection_name: str):
    """Get a collection from the database."""
    return get_database()[collection_name]
