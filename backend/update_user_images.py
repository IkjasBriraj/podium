"""
Update user images in MongoDB with S3 URLs and placeholder images
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from motor.motor_asyncio import AsyncIOMotorClient
from backend.config import get_settings

settings = get_settings()

# S3 base URL
S3_BASE = f"https://{settings.s3_bucket_name}.s3.{settings.aws_region}.amazonaws.com"

# Updated image URLs - mix of S3 uploaded and high-quality placeholders
USER_IMAGES = {
    "athlete1": {  # PV Sindhu
        "profile_image": f"{S3_BASE}/profiles/athlete1_profile.png",
        "cover_image": f"{S3_BASE}/covers/athlete1_cover.png"
    },
    "athlete2": {  # Kento Momota
        "profile_image": f"{S3_BASE}/profiles/athlete2_profile.png",
        "cover_image": f"{S3_BASE}/covers/athlete2_cover.png"
    },
    "athlete3": {  # An Se Young
        "profile_image": f"{S3_BASE}/profiles/athlete3_profile.png",
        "cover_image": "https://images.unsplash.com/photo-1626224583764-847890e0e99b?q=80&w=2070"  # Placeholder cover
    },
    "athlete4": {  # Viktor Axelsen
        "profile_image": "https://images.unsplash.com/photo-1552374196-1ab2a1c593e8?w=800&h=800&fit=crop",  # Athletic male placeholder
        "cover_image": "https://images.unsplash.com/photo-1626224583764-847890e0e99b?q=80&w=2070"
    },
    "athlete5": {  # Lee Chong Wei
        "profile_image": "https://images.unsplash.com/photo-1566753323558-f4e0952af115?w=800&h=800&fit=crop",  # Mature athlete placeholder
        "cover_image": "https://images.unsplash.com/photo-1626224583764-847890e0e99b?q=80&w=2070"
    },
    "coach1": {  # Pullela Gopichand
        "profile_image": "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=800&h=800&fit=crop",  # Coach placeholder
        "cover_image": "https://images.unsplash.com/photo-1626224583764-847890e0e99b?q=80&w=2070"
    },
    "coach2": {  # Park Joo-bong
        "profile_image": "https://images.unsplash.com/photo-1552374196-1ab2a1c593e8?w=800&h=800&fit=crop",  # Mature coach placeholder
        "cover_image": "https://images.unsplash.com/photo-1626224583764-847890e0e99b?q=80&w=2070"
    }
}

async def update_images():
    """Update user images in MongoDB"""
    print("\n" + "="*70)
    print("UPDATING USER IMAGES IN MONGODB")
    print("="*70 + "\n")
    
    client = AsyncIOMotorClient(settings.mongodb_url, serverSelectionTimeoutMS=5000)
    db = client[settings.db_name]
    
    try:
        await client.server_info()
        print("✓ Connected to MongoDB\n")
        
        for user_id, images in USER_IMAGES.items():
            result = await db["users"].update_one(
                {"_id": user_id},
                {"$set": {
                    "profile_image": images["profile_image"],
                    "cover_image": images["cover_image"]
                }}
            )
            
            if result.matched_count > 0:
                print(f"✓ Updated {user_id}")
                print(f"  Profile: {images['profile_image'][:80]}...")
                print(f"  Cover: {images['cover_image'][:80]}...")
            else:
                print(f"✗ User {user_id} not found")
        
        print("\n" + "="*70)
        print("IMAGE UPDATE COMPLETE")
        print("="*70)
        
        # Verify updates
        print("\n📊 Verification:")
        users = await db["users"].find({}, {"_id": 1, "name": 1, "profile_image": 1, "cover_image": 1}).to_list(100)
        for user in users:
            has_profile = "✓" if user.get("profile_image") else "✗"
            has_cover = "✓" if user.get("cover_image") else "✗"
            print(f"  {user['name']:25} - Profile: {has_profile}  Cover: {has_cover}")
        
        print("\n✅ All images updated successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()
        print("\n✓ Disconnected from MongoDB\n")

if __name__ == "__main__":
    asyncio.run(update_images())
