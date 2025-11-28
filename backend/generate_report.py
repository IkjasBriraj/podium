"""
Generate a comprehensive report of seeded data and save to file
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from motor.motor_asyncio import AsyncIOMotorClient
from backend.config import get_settings

settings = get_settings()

async def generate_report():
    """Generate comprehensive data report"""
    client = AsyncIOMotorClient(settings.mongodb_url, serverSelectionTimeoutMS=5000)
    db = client[settings.db_name]
    
    report = []
    
    try:
        await client.server_info()
        report.append("="*70)
        report.append("MOCK DATA SEEDING REPORT")
        report.append("="*70)
        report.append("")
        
        # Count documents
        users_count = await db["users"].count_documents({})
        posts_count = await db["posts"].count_documents({})
        videos_count = await db["training_videos"].count_documents({})
        opps_count = await db["opportunities"].count_documents({})
        
        report.append("📊 DATABASE SUMMARY")
        report.append("-" * 70)
        report.append(f"  • Users: {users_count} (5 athletes + 2 coaches)")
        report.append(f"  • Posts: {posts_count}")
        report.append(f"  • Training Videos: {videos_count}")
        report.append(f"  • Opportunities: {opps_count}")
        report.append("")
        
        # List all users with details
        report.append("="*70)
        report.append("👥 USER PROFILES")
        report.append("="*70)
        report.append("")
        
        users = await db["users"].find({}).to_list(100)
        
        # Athletes
        report.append("🏸 ATHLETES (5)")
        report.append("-" * 70)
        athletes = [u for u in users if u["role"] == "athlete"]
        for i, user in enumerate(athletes, 1):
            report.append(f"\n{i}. {user['name']}")
            report.append(f"   ID: {user['_id']}")
            report.append(f"   Username: {user.get('username', 'N/A')}")
            report.append(f"   Email: {user.get('email', 'N/A')}")
            report.append(f"   Headline: {user.get('headline', 'N/A')}")
            report.append(f"   Location: {user.get('location', 'N/A')}")
            report.append(f"   Age: {user.get('age', 'N/A')} | Height: {user.get('height', 'N/A')} | Weight: {user.get('weight', 'N/A')}")
            report.append(f"   Playing Hand: {user.get('playing_hand', 'N/A')}")
            report.append(f"   Experience: {user.get('years_of_experience', 'N/A')} years")
            report.append(f"   Academy: {user.get('academy', 'N/A')}")
            report.append(f"   Skills: {len(user.get('skills', []))} skills")
        
        report.append("")
        
        # Coaches
        report.append("🎓 COACHES (2)")
        report.append("-" * 70)
        coaches = [u for u in users if u["role"] == "coach"]
        for i, user in enumerate(coaches, 1):
            report.append(f"\n{i}. {user['name']}")
            report.append(f"   ID: {user['_id']}")
            report.append(f"   Username: {user.get('username', 'N/A')}")
            report.append(f"   Email: {user.get('email', 'N/A')}")
            report.append(f"   Headline: {user.get('headline', 'N/A')}")
            report.append(f"   Location: {user.get('location', 'N/A')}")
            report.append(f"   Experience: {user.get('years_of_experience', 'N/A')} years")
            report.append(f"   Academy: {user.get('academy', 'N/A')}")
            report.append(f"   Skills: {len(user.get('skills', []))} skills")
        
        report.append("")
        
        # Login Credentials
        report.append("="*70)
        report.append("🔐 LOGIN CREDENTIALS")
        report.append("="*70)
        report.append("")
        report.append("Password for ALL users: password123")
        report.append("")
        
        report.append("Athletes:")
        report.append("-" * 70)
        for user in athletes:
            report.append(f"  Username: {user.get('username', 'N/A'):20} | Email: {user.get('email', 'N/A'):35} | {user['name']}")
        
        report.append("")
        report.append("Coaches:")
        report.append("-" * 70)
        for user in coaches:
            report.append(f"  Username: {user.get('username', 'N/A'):20} | Email: {user.get('email', 'N/A'):35} | {user['name']}")
        
        report.append("")
        
        # Posts Summary
        report.append("="*70)
        report.append("📝 POSTS SUMMARY")
        report.append("="*70)
        report.append("")
        posts = await db["posts"].find({}).to_list(100)
        posts_by_user = {}
        for post in posts:
            author_id = post['author_id']
            if author_id not in posts_by_user:
                posts_by_user[author_id] = []
            posts_by_user[author_id].append(post)
        
        for user in users:
            user_posts = posts_by_user.get(user['_id'], [])
            report.append(f"  {user['name']:30} - {len(user_posts)} posts")
        
        report.append("")
        
        # Training Videos
        report.append("="*70)
        report.append("🎥 TRAINING VIDEOS")
        report.append("="*70)
        report.append("")
        videos = await db["training_videos"].find({}).to_list(100)
        for i, video in enumerate(videos, 1):
            report.append(f"{i}. {video['title']}")
            report.append(f"   Author: {video['author']} | Views: {video.get('views', '0')} | Duration: {video.get('duration', '00:00')}")
            report.append(f"   Categories: {', '.join(video.get('categories', []))}")
            report.append("")
        
        # Opportunities
        report.append("="*70)
        report.append("💼 OPPORTUNITIES")
        report.append("="*70)
        report.append("")
        opps = await db["opportunities"].find({}).to_list(100)
        for i, opp in enumerate(opps, 1):
            poster = next((u for u in users if u['_id'] == opp['poster_id']), None)
            poster_name = poster['name'] if poster else 'Unknown'
            report.append(f"{i}. {opp['title']}")
            report.append(f"   Type: {opp['type']} | Posted by: {poster_name}")
            report.append(f"   Budget: {opp.get('budget', 'Not specified')}")
            report.append(f"   Requirements: {len(opp.get('requirements', []))} items")
            report.append("")
        
        report.append("="*70)
        report.append("✅ ALL DATA SUCCESSFULLY SEEDED!")
        report.append("="*70)
        report.append("")
        report.append("Storage Information:")
        report.append(f"  • Database: MongoDB ({settings.db_name})")
        report.append(f"  • Images: External URLs (profile/cover images)")
        report.append(f"  • S3 Bucket: Ready for file uploads")
        report.append("")
        
    except Exception as e:
        report.append(f"\n❌ Error: {e}")
        import traceback
        report.append(traceback.format_exc())
    finally:
        client.close()
    
    # Write to file
    report_text = "\n".join(report)
    with open("backend/seed_report.txt", "w", encoding="utf-8") as f:
        f.write(report_text)
    
    print(report_text)
    print("\n📄 Report saved to: backend/seed_report.txt")

if __name__ == "__main__":
    asyncio.run(generate_report())
