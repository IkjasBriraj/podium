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
        title=title,
        author=author,
        description=description,
        type=type,
        video_url=video_url,
        file=file,
        storage=storage
    )


@router.post("/training/analyze-video")
async def analyze_video(file: UploadFile = File(...)):
    """Analyze video using local Ollama model"""
    import shutil
    import tempfile
    import os
    import traceback
    from backend.app.services.ollama_service import OllamaService
    
    print(f"Received video upload: {file.filename}")
    
    # Create temp file
    suffix = os.path.splitext(file.filename)[1]
    if not suffix: suffix = ".mp4"
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
        
        print(f"Saved temp video to: {tmp_path}")
            
        # Run analysis
        try:
            print("Starting OllamaService analysis...")
            service = OllamaService()
            result = await service.analyze_video(tmp_path)
            print("Analysis complete.")
            return result
        except Exception as e:
            print(f"Error during analysis: {str(e)}")
            traceback.print_exc()
            from fastapi import HTTPException
            raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    except Exception as e:
        print(f"Error handling upload: {str(e)}")
        traceback.print_exc()
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"Upload processing failed: {str(e)}")
    finally:
        # Cleanup
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
                print(f"Cleaned up temp file: {tmp_path}")
            except Exception as e:
                print(f"Failed to cleanup temp file: {e}")
