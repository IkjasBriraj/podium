from typing import List, Optional, Dict, Any


class PostRepository:
    """Repository for post data access"""
    
    def __init__(self, db):
        self.db = db
        self.collection = db["posts"]
        self.comments_collection = db["comments"]
    
    async def get_all(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all posts (feed)"""
        return await self.collection.find().sort("_id", -1).to_list(limit)
    
    async def get_by_id(self, post_id: str) -> Optional[Dict[str, Any]]:
        """Get post by ID"""
        return await self.collection.find_one({"_id": post_id})
    
    async def get_by_user_id(self, user_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get posts by user ID"""
        return await self.collection.find({"author_id": user_id}).sort("_id", -1).to_list(limit)
    
    async def create(self, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new post"""
        await self.collection.insert_one(post_data)
        return post_data
    
    async def increment_likes(self, post_id: str) -> Optional[int]:
        """Increment like count for a post"""
        result = await self.collection.update_one(
            {"_id": post_id},
            {"$inc": {"likes": 1}}
        )
        if result.matched_count == 0:
            return None
        post = await self.get_by_id(post_id)
        return post["likes"] if post else None
    
    async def increment_comments(self, post_id: str) -> None:
        """Increment comment count for a post"""
        await self.collection.update_one(
            {"_id": post_id},
            {"$inc": {"comments": 1}}
        )
    
    async def get_comments(self, post_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get comments for a post"""
        return await self.comments_collection.find({"post_id": post_id}).sort("created_at", 1).to_list(limit)
    
    async def create_comment(self, comment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new comment"""
        await self.comments_collection.insert_one(comment_data)
        return comment_data
