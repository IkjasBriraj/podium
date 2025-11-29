from fastapi import UploadFile, HTTPException
import os


class MediaService:
    """Service for media file validation and upload operations"""
    
    @staticmethod
    def validate_media_file(file: UploadFile) -> bool:
        """Validate media file type"""
        allowed_types = [
            "image/jpeg", "image/png", "image/jpg", "image/webp",
            "video/mp4", "video/webm"
        ]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
            )
        return True
    
    @staticmethod
    def upload_with_custom_filename(file: UploadFile, folder: str, custom_filename: str, storage):
        """Upload file with custom filename"""
        MediaService.validate_media_file(file)
        return storage.upload_file(file, folder=folder, custom_filename=custom_filename)
    
    @staticmethod
    def upload_file(file: UploadFile, folder: str, storage):
        """Upload file with generated filename"""
        MediaService.validate_media_file(file)
        return storage.upload_file(file, folder=folder)
