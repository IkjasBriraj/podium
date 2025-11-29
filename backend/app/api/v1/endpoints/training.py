from fastapi import APIRouter, Form, File, UploadFile, Response
from typing import List, Optional
from backend.app.schemas.training import TrainingVideo
from backend.app.db.mongodb import db
from backend.app.db.repositories.training_repository import TrainingRepository
from backend.app.services.training_service import TrainingService
from backend.app.infrastructure.storage import storage

router = APIRouter()


@router.get("/training/videos", response_model=List[TrainingVideo])
async def get_training_videos(response: Response):
    """Get all training videos"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    training_repo = TrainingRepository(db.get_db())
    training_service = TrainingService(training_repo)
    return await training_service.get_training_videos()


@router.post("/training/videos", response_model=TrainingVideo)
async def create_training_video(
    title: str = Form(...),
    author: str = Form(...),
    description: str = Form(None),
    type: str = Form(...),
    video_url: str = Form(None),
    file: Optional[UploadFile] = File(None)
):
    """Create new training video"""
    training_repo = TrainingRepository(db.get_db())
    training_service = TrainingService(training_repo)
    return await training_service.create_training_video(
        title, author, description, type, video_url, file, storage
    )
