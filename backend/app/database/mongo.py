from motor.motor_asyncio import AsyncClient, AsyncDatabase
from typing import Optional
from app.config import settings

class Database:
    client: Optional[AsyncClient] = None
    db: Optional[AsyncDatabase] = None

db = Database()

async def connect_db():
    """Create database connection."""
    db.client = AsyncClient(settings.DATABASE_URL)
    db.db = db.client[settings.DATABASE_NAME]
    
    # Create indexes
    await create_indexes()
    print("✓ Database connected")

async def close_db():
    """Close database connection."""
    if db.client:
        db.client.close()
        print("✓ Database disconnected")

async def create_indexes():
    """Create database indexes for better performance."""
    if not db.db:
        return
    
    # Users indexes
    await db.db.users.create_index("email", unique=True)
    await db.db.users.create_index("created_at")
    
    # Resumes indexes
    await db.db.resumes.create_index("user_id")
    await db.db.resumes.create_index("created_at")
    await db.db.resumes.create_index([("user_id", 1), ("created_at", -1)])
    
    # Analyses indexes
    await db.db.analyses.create_index("resume_id")
    await db.db.analyses.create_index("user_id")
    await db.db.analyses.create_index("created_at")
    
    # Job matches indexes
    await db.db.job_matches.create_index("resume_id")
    await db.db.job_matches.create_index("user_id")
    await db.db.job_matches.create_index("created_at")
    
    # Activity logs indexes
    await db.db.activity_logs.create_index("user_id")
    await db.db.activity_logs.create_index("timestamp")
    
    # Refresh tokens indexes
    await db.db.refresh_tokens.create_index("user_id")
    await db.db.refresh_tokens.create_index("expires_at", expireAfterSeconds=0)

def get_db():
    """Get database instance."""
    return db.db
