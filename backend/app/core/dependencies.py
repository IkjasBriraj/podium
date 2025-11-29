from backend.app.db.mongodb import get_database

async def get_db():
    """Dependency for getting database instance"""
    return await get_database()
