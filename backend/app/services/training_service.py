from fastapi import HTTPException, UploadFile
from typing import List, Optional, Dict, Any
from backend.app.db.repositories.training_repository import TrainingRepository, OpportunityRepository
from backend.app.services.media_service import MediaService
import uuid
import re


class TrainingService:
    """Service for training video business logic"""
    
    def __init__(self, training_repository: TrainingRepository):
        self.training_repo = training_repository
    
    async def get_training_videos(self) -> List[Dict[str, Any]]:
        """Get all training videos"""
        return await self.training_repo.get_all()
    
    async def create_training_video(
        self,
        title: str,
        author: str,
        description: Optional[str],
        type: str,
        video_url: Optional[str],
        file: Optional[UploadFile],
        storage
    ) -> Dict[str, Any]:
        """Create new training video"""
        final_video_url = video_url
        thumbnail_url = None
        
        if type == 'file':
            if not file:
                raise HTTPException(status_code=400, detail="File is required for file upload type")
            final_video_url = MediaService.upload_file(file, "training", storage)
            thumbnail_url = None
        
        elif type == 'link':
            if not video_url:
                raise HTTPException(status_code=400, detail="Video URL is required for link type")
            
            # Extract YouTube ID
            video_id = self.extract_youtube_id(video_url)
            if video_id:
                final_video_url = video_id
                thumbnail_url = f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"
        
        video_id = str(uuid.uuid4())
        new_video = {
            "_id": video_id,
            "title": title,
            "author": author,
            "description": description,
            "video_url": final_video_url,
            "thumbnail_url": thumbnail_url,
            "duration": "00:00",
            "views": "0",
            "type": type,
            "analysis": None
        }
        
        return await self.training_repo.create(new_video)
    
    @staticmethod
    def extract_youtube_id(url: str) -> Optional[str]:
        """Extract YouTube video ID from URL"""
        youtube_regex = (
            r'(https?://)?(www\.)?'
            r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
            r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
        )
        
        match = re.match(youtube_regex, url)
        if match:
            return match.group(6)
        return None


class OpportunityService:
    """Service for opportunity business logic"""
    
    def __init__(self, opportunity_repository: OpportunityRepository):
        self.opportunity_repo = opportunity_repository
    
    async def get_opportunities(self) -> List[Dict[str, Any]]:
        """Get all opportunities"""
        return await self.opportunity_repo.get_all()
