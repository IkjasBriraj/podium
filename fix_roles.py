import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def fix_roles():
    client = AsyncIOMotorClient("mongodb://admin:P%40ssw0rd@localhost:27017/")
    db = client["podium_db"]
    
    # Update all users with 'Athlete' to 'athlete'
    result = await db.users.update_many(
        {"role": "Athlete"},
        {"$set": {"role": "athlete"}}
    )
    print(f"Updated {result.modified_count} user(s): Athlete -> athlete")
    
    # Also update 'Coach' to 'coach' for consistency
    result2 = await db.users.update_many(
        {"role": "Coach"},
        {"$set": {"role": "coach"}}
    )
    print(f"Updated {result2.modified_count} user(s): Coach -> coach")
    
    client.close()
    print("Done! Please log out and log back in with Google to see the fix.")

if __name__ == "__main__":
    asyncio.run(fix_roles())
