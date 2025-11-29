from typing import List, Dict, Any


class TrainingRepository:
    """Repository for training video data access"""
    
    def __init__(self, db):
        self.db = db
        self.collection = db["training_videos"]
    
    async def get_all(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all training videos"""
        return await self.collection.find().sort("_id", -1).to_list(limit)
    
    async def create(self, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new training video"""
        await self.collection.insert_one(video_data)
        return video_data


class OpportunityRepository:
    """Repository for opportunity data access"""
    
    def __init__(self, db):
        self.db = db
        self.collection = db["opportunities"]
    
    async def get_all(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all opportunities"""
        return await self.collection.find().to_list(limit)
