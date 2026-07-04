"""MongoDB connection and management."""

import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config import settings

logger = logging.getLogger(__name__)

client: AsyncIOMotorClient | None = None
db: AsyncIOMotorDatabase | None = None


async def connect_db():
    """Connect to MongoDB."""
    global client, db
    try:
        client = AsyncIOMotorClient(settings.DATABASE_URL)
        db = client[settings.DATABASE_NAME]
        
        # Test connection
        await db.command("ping")
        logger.info(f"Connected to MongoDB: {settings.DATABASE_NAME}")
        
        # Create collections if they don't exist
        collections = await db.list_collection_names()
        
        if "users" not in collections:
            await db.create_collection("users")
            await db.users.create_index("email", unique=True)
            logger.info("Created 'users' collection with unique email index")
        
        if "resumes" not in collections:
            await db.create_collection("resumes")
            await db.resumes.create_index([("user_id", 1), ("created_at", -1)])
            logger.info("Created 'resumes' collection")
        
        if "analyses" not in collections:
            await db.create_collection("analyses")
            await db.analyses.create_index([("resume_id", 1), ("created_at", -1)])
            logger.info("Created 'analyses' collection")
        
        if "job_matches" not in collections:
            await db.create_collection("job_matches")
            await db.job_matches.create_index([("resume_id", 1), ("created_at", -1)])
            logger.info("Created 'job_matches' collection")
        
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise


async def close_db():
    """Close MongoDB connection."""
    global client

    if client:
        client.close()
        logger.info("MongoDB connection closed")


def get_db() -> AsyncIOMotorDatabase:
    """Return the MongoDB database instance."""
    if db is None:
        raise RuntimeError("Database connection has not been initialized.")
    return db