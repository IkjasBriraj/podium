from fastapi import HTTPException, UploadFile
from typing import List, Optional, Dict, Any
from backend.app.db.repositories.post_repository import PostRepository
from backend.app.services.media_service import MediaService
from datetime import datetime
import uuid


class PostService:
    """Service for post business logic"""
    
    def __init__(self, post_repository: PostRepository):
        self.post_repo = post_repository
    
    async def get_feed(self) -> List[Dict[str, Any]]:
        """Get feed posts"""
        return await self.post_repo.get_all()
    
    async def get_user_posts(self, user_id: str) -> List[Dict[str, Any]]:
        """Get posts by user"""
        return await self.post_repo.get_by_user_id(user_id)
    
    async def create_post(
        self, 
        user_id: str, 
        content: str, 
        type: str, 
        file: Optional[UploadFile], 
        storage
    ) -> Dict[str, Any]:
        """Create new post"""
        media_url = None
        if file:
            media_url = MediaService.upload_file(file, "posts", storage)
        
        post_id = str(uuid.uuid4())
        new_post = {
            "_id": post_id,
            "author_id": user_id,
            "content": content,
            "media_url": media_url,
            "type": type,
            "likes": 0,
            "comments": 0
        }
        
        return await self.post_repo.create(new_post)
    
    async def like_post(self, post_id: str) -> Dict[str, int]:
        """Like a post"""
        likes_count = await self.post_repo.increment_likes(post_id)
        if likes_count is None:
            raise HTTPException(status_code=404, detail="Post not found")
        return {"likes": likes_count}
    
    async def get_comments(self, post_id: str) -> List[Dict[str, Any]]:
        """Get comments for a post"""
        return await self.post_repo.get_comments(post_id)
    
    async def add_comment(self, post_id: str, author_id: str, content: str) -> Dict[str, Any]:
        """Add comment to a post"""
        # Verify post exists
        post = await self.post_repo.get_by_id(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        new_comment = {
            "_id": str(uuid.uuid4()),
            "post_id": post_id,
            "author_id": author_id,
            "content": content,
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Create comment
        comment = await self.post_repo.create_comment(new_comment)
        
        # Increment comment count on post
        await self.post_repo.increment_comments(post_id)
        
        return comment
