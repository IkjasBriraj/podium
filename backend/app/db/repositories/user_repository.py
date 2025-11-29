from typing import List, Optional, Dict, Any


class UserRepository:
    """Repository for user data access"""
    
    def __init__(self, db):
        self.db = db
        self.collection = db["users"]
    
    async def get_all(self, limit: int = 1000) -> List[Dict[str, Any]]:
        """Get all users"""
        return await self.collection.find().to_list(limit)
    
    async def get_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        return await self.collection.find_one({"_id": user_id})
    
    async def create(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new user"""
        await self.collection.insert_one(user_data)
        return user_data
    
    async def update(self, user_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update user"""
        result = await self.collection.update_one(
            {"_id": user_id},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            return None
        return await self.get_by_id(user_id)
    
    async def update_profile_image(self, user_id: str, image_url: str) -> Optional[Dict[str, Any]]:
        """Update user's profile image"""
        return await self.update(user_id, {"profile_image": image_url})
    
    async def update_cover_image(self, user_id: str, image_url: str) -> Optional[Dict[str, Any]]:
        """Update user's cover image"""
        return await self.update(user_id, {"cover_image": image_url})
