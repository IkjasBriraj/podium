from fastapi import HTTPException, UploadFile
from typing import List, Optional, Dict, Any
from backend.app.db.repositories.user_repository import UserRepository
from backend.app.services.media_service import MediaService
import uuid
import os


class UserService:
    """Service for user business logic"""
    
    def __init__(self, user_repository: UserRepository):
        self.user_repo = user_repository
    
    async def get_users(self) -> List[Dict[str, Any]]:
        """Get all users"""
        return await self.user_repo.get_all()
    
    async def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get user by ID"""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    async def get_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user profile"""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Profile not found")
        return user
    
    async def create_profile(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new user profile"""
        user_id = str(uuid.uuid4())
        
        new_user = profile_data.copy()
        new_user["_id"] = user_id
        new_user["profile_image"] = None
        new_user["cover_image"] = None
        new_user["skills"] = []
        new_user["experience"] = []
        # Initialize other fields
        for field in ["age", "weight", "height", "playing_hand", "years_of_experience", "age_category", "academy"]:
            new_user[field] = None
        
        return await self.user_repo.create(new_user)
    
    async def update_profile(self, user_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user profile"""
        if not update_data:
            # No update data, just return existing user
            user = await self.user_repo.get_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="Profile not found")
            return user
        
        updated_user = await self.user_repo.update(user_id, update_data)
        if not updated_user:
            raise HTTPException(status_code=404, detail="Profile not found")
        return updated_user
    
    async def upload_profile_image(self, user_id: str, file: UploadFile, storage) -> Dict[str, str]:
        """Upload profile image"""
        # Verify user exists
        user = await self.user_repo.get_by_id(user_id)
        print(f"IN upload_profile_image: {user_id}, user: {user}")
        if not user:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        # Generate consistent filename so new uploads overwrite old ones
        file_extension = os.path.splitext(file.filename)[1]
        custom_filename = f"{user_id}_profile{file_extension}"
        
        # Upload to S3
        image_url = MediaService.upload_with_custom_filename(file, "profiles", custom_filename, storage)
        print(f"IN upload_profile_image: image_url: {image_url}")
        
        # Update DB
        await self.user_repo.update_profile_image(user_id, image_url)
        
        return {"message": "Profile image uploaded", "image_url": image_url}
    
    async def upload_cover_image(self, user_id: str, file: UploadFile, storage) -> Dict[str, str]:
        """Upload cover image"""
        # Verify user exists
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        # Generate consistent filename so new uploads overwrite old ones
        file_extension = os.path.splitext(file.filename)[1]
        custom_filename = f"{user_id}_cover{file_extension}"
        
        # Upload to S3
        image_url = MediaService.upload_with_custom_filename(file, "covers", custom_filename, storage)
        
        # Update DB
        await self.user_repo.update_cover_image(user_id, image_url)
        
        return {"message": "Cover image uploaded", "image_url": image_url}
