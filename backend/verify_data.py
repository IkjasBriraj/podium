"""
Verify the seeded data in MongoDB
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from motor.motor_asyncio import AsyncIOMotorClient
from backend.config import get_settings

settings = get_settings()

async def verify_data():
    """Verify seeded data"""
    client = AsyncIOMotorClient(settings.mongodb_url, serverSelectionTimeoutMS=5000)
    db = client[settings.db_name]
    
    try:
        await client.server_info()
        print("✓ Connected to MongoDB\n")
        
        # Count documents in each collection
        users_count = await db["users"].count_documents({})
        posts_count = await db["posts"].count_documents({})
        videos_count = await db["training_videos"].count_documents({})
        opps_count = await db["opportunities"].count_documents({})
        
        print("📊 Database Contents:")
        print(f"  • Users: {users_count}")
        print(f"  • Posts: {posts_count}")
        print(f"  • Training Videos: {videos_count}")
        print(f"  • Opportunities: {opps_count}")
        print()
        
        # List all users
        print("👥 Users in database:")
        users = await db["users"].find({}, {"_id": 1, "name": 1, "role": 1, "username": 1}).to_list(100)
        for user in users:
            print(f"  {user['_id']:12} - {user['name']:25} ({user['role']:8}) - username: {user.get('username', 'N/A')}")
        
        print("\n✅ Verification complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(verify_data())
