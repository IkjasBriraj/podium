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
        except Exception as e:
            print(f"✗ MongoDB connection failed: {e}")
            print("⚠ Running with in-memory storage - data will not persist!")
            self.connected = False
            self.memory_db = InMemoryDatabase()
            self._seed_memory_db()

    def _seed_memory_db(self):
        """Seed in-memory database with sample data"""
        import asyncio
        asyncio.create_task(self._async_seed())
    
    async def _async_seed(self):
        """Async seed function"""
        # Seed sample user
        await self.memory_db["users"].insert_one({
            "_id": "u1",
            "name": "Lee Chong Wei",
            "role": "athlete",
            "sport": "Badminton",
            "headline": "3x Olympic Silver Medalist | Brand Ambassador",
            "bio": "Professional badminton player with over 20 years of experience.",
            "location": "Kuala Lumpur, Malaysia",
            "category": "Singles",
            "profile_image": None,
            "cover_image": None,
            "age": 41,
            "weight": "60 kg",
            "height": "172 cm",
            "playing_hand": "Right",
            "years_of_experience": 25,
            "age_category": "Senior",
            "academy": "Bukit Jalil Sports School",
            "skills": [
                {"name": "Smash", "endorsements": 45},
                {"name": "Net Play", "endorsements": 32}
            ],
            "experience": [{
                "role": "National Team Player",
                "org": "Badminton Association of Malaysia (BAM)",
                "years": "2000 - 2019",
                "description": "Represented Malaysia in 4 Olympic Games."
            }]
        })
        
        # Seed training videos
        await self.memory_db["training_videos"].insert_one({
            "_id": "v1",
            "title": "Badminton Smash",
            "author": "Lee Chong Wei",
            "description": "Learn powerful smash techniques.",
            "video_url": "s3cMVBRmySc",
            "thumbnail_url": "https://img.youtube.com/vi/s3cMVBRmySc/mqdefault.jpg",
            "duration": "12:45",
            "views": "234K",
            "type": "link",
            "analysis": None
        })

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
