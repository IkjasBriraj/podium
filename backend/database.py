from motor.motor_asyncio import AsyncIOMotorClient
from backend.config import get_settings
from backend.memory_db import InMemoryDatabase
import sys

settings = get_settings()

class Database:
    client: AsyncIOMotorClient = None
    connected: bool = False
    memory_db: InMemoryDatabase = None

    def connect(self):
        try:
            self.client = AsyncIOMotorClient(settings.mongodb_url, serverSelectionTimeoutMS=5000)
            # Test connection
            self.client.server_info()
            self.connected = True
            print("✓ Connected to MongoDB")
            self._seed_db() # Seed even if connected
        except Exception as e:
            print(f"✗ MongoDB connection failed: {e}")
            print("⚠ Running with in-memory storage - data will not persist!")
            self.connected = False
            self.memory_db = InMemoryDatabase()
            self._seed_db()

    def _seed_db(self):
        """Seed database with sample data"""
        import asyncio
        # Create a new loop if needed or use existing
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        if loop.is_running():
            # We are likely in the startup event loop
            asyncio.create_task(self.seed_data())
        else:
            loop.run_until_complete(self.seed_data())
    
    async def seed_data(self):
        """Async seed function"""
        db = self.get_db()
        
        # Seed sample user (Upsert)
        await db["users"].update_one(
            {"_id": "u1"},
            {"$set": {
                "name": "Lee Chong Wei",
                "role": "athlete",
                "sport": "Badminton",
                "headline": "3x Olympic Silver Medalist | Brand Ambassador",
                "bio": "Professional badminton player with over 20 years of experience. Former World No. 1 for 349 weeks.",
                "location": "Kuala Lumpur, Malaysia",
                "category": "Singles",
                "profile_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Lee_Chong_Wei_at_French_Open_2013.jpg/800px-Lee_Chong_Wei_at_French_Open_2013.jpg",
                "cover_image": "https://images.unsplash.com/photo-1626224583764-847890e0e99b?q=80&w=2070&auto=format&fit=crop",
                "age": 41,
                "weight": "60 kg",
                "height": "172 cm",
                "playing_hand": "Right",
                "years_of_experience": 25,
                "age_category": "Senior",
                "academy": "Bukit Jalil Sports School",
                "skills": [
                    {"name": "Smash", "endorsements": 1500},
                    {"name": "Net Play", "endorsements": 1200},
                    {"name": "Defense", "endorsements": 980},
                    {"name": "Footwork", "endorsements": 1100}
                ],
                "experience": [
                    {
                        "role": "National Team Player",
                        "org": "Badminton Association of Malaysia (BAM)",
                        "years": "2000 - 2019",
                        "description": "Represented Malaysia in 4 Olympic Games, winning 3 Silver medals."
                    },
                    {
                        "role": "Brand Ambassador",
                        "org": "Yonex",
                        "years": "2005 - Present",
                        "description": "Global ambassador for Yonex badminton equipment."
                    }
                ]
            }},
            upsert=True
        )
        
        # Seed sample posts (Check if exists first to avoid dupes if no ID, but we use ID p1)
        if not await db["posts"].find_one({"_id": "p1"}):
            await db["posts"].insert_one({
                "_id": "p1",
                "author_id": "u1",
                "content": "Great training session today! Focusing on speed and agility. 🏸 #badminton #training",
                "media_url": None,
                "type": "text",
                "likes": 245,
                "comments": 12
            })

        # Seed training videos
        videos = [
            {
                "_id": "v1",
                "title": "Advanced Footwork Drills",
                "author": "An Se Young",
                "description": "Master the court coverage with these essential footwork patterns.",
                "video_url": "QIBIvy9hB8I",
                "thumbnail_url": "https://img.youtube.com/vi/QIBIvy9hB8I/mqdefault.jpg",
                "duration": "10:15",
                "views": "1.2M",
                "type": "link",
                "categories": ["footwork", "technique"],
                "analysis": None
            },
            {
                "_id": "v2",
                "title": "Ultimate Smash Masterclass",
                "author": "Lee Chong Wei",
                "description": "Learn the technique behind one of the fastest smashes in the world.",
                "video_url": "s3cMVBRmySc",
                "thumbnail_url": "https://img.youtube.com/vi/s3cMVBRmySc/mqdefault.jpg",
                "duration": "12:45",
                "views": "3.5M",
                "type": "link",
                "categories": ["technique"],
                "analysis": None
            },
            {
                "_id": "v3",
                "title": "Net Play Secrets",
                "author": "Kento Momota",
                "description": "Dominate the front court with deceptive net shots.",
                "video_url": "Zj_jdy1GWOc",
                "thumbnail_url": "https://img.youtube.com/vi/Zj_jdy1GWOc/mqdefault.jpg",
                "duration": "08:30",
                "views": "890K",
                "type": "link",
                "categories": ["technique"],
                "analysis": None
            },
            {
                "_id": "v4",
                "title": "Master Footwork",
                "author": "Lin Dan",
                "description": "Legendary footwork techniques from the GOAT.",
                "video_url": "yxBVlMncudg",
                "thumbnail_url": "https://img.youtube.com/vi/yxBVlMncudg/mqdefault.jpg",
                "duration": "15:20",
                "views": "2.1M",
                "type": "link",
                "categories": ["footwork"],
                "analysis": None
            },
            {
                "_id": "v5",
                "title": "4 Corner Footwork Tutorial",
                "author": "Badminton Insight",
                "description": "Step-by-step guide to mastering movement to all four corners.",
                "video_url": "R_Qz-D18fV0",
                "thumbnail_url": "https://img.youtube.com/vi/R_Qz-D18fV0/mqdefault.jpg",
                "duration": "09:45",
                "views": "560K",
                "type": "link",
                "categories": ["footwork"],
                "analysis": None
            },
            {
                "_id": "v6",
                "title": "Offensive Net Footwork",
                "author": "Basicfeather",
                "description": "Aggressive footwork to dominate the net area.",
                "video_url": "0V1t2IHEFxQ",
                "thumbnail_url": "https://img.youtube.com/vi/0V1t2IHEFxQ/mqdefault.jpg",
                "duration": "07:12",
                "views": "320K",
                "type": "link",
                "categories": ["footwork"],
                "analysis": None
            }
        ]
        
        for video in videos:
            await db["training_videos"].update_one(
                {"_id": video["_id"]},
                {"$set": video},
                upsert=True
            )

    def close(self):
        if self.client:
            self.client.close()
            print("Disconnected from MongoDB")

    def get_db(self):
        if self.connected:
            return self.client[settings.db_name]
        else:
            return self.memory_db

db = Database()

async def get_database():
    return db.get_db()
