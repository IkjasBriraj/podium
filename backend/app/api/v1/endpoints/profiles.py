from fastapi import APIRouter, File, UploadFile
from backend.app.schemas.user import User, ProfileCreateRequest, ProfileUpdateRequest
from backend.app.db.mongodb import db
from backend.app.db.repositories.user_repository import UserRepository
from backend.app.services.user_service import UserService
from backend.app.infrastructure.storage import storage
import traceback

router = APIRouter()


@router.get("/profiles/{user_id}", response_model=User)
async def get_profile(user_id: str):
    """Get user profile"""
    user_repo = UserRepository(db.get_db())
    user_service = UserService(user_repo)
    return await user_service.get_profile(user_id)


@router.post("/profiles", response_model=User)
async def create_profile(profile: ProfileCreateRequest):
    """Create new profile"""
    user_repo = UserRepository(db.get_db())
    user_service = UserService(user_repo)
    return await user_service.create_profile(profile.model_dump())


@router.put("/profiles/{user_id}", response_model=User)
async def update_profile(user_id: str, profile: ProfileUpdateRequest):
    """Update profile"""
    user_repo = UserRepository(db.get_db())
    user_service = UserService(user_repo)
    return await user_service.update_profile(user_id, profile.model_dump(exclude_unset=True))


@router.post("/profiles/{user_id}/image")
async def upload_profile_image(user_id: str, file: UploadFile = File(...)):
    """Upload profile image"""
    try:
        user_repo = UserRepository(db.get_db())
        user_service = UserService(user_repo)
        return await user_service.upload_profile_image(user_id, file, storage)
    except Exception as e:
        traceback.print_exc()
        raise


@router.post("/profiles/{user_id}/cover")
async def upload_cover_image(user_id: str, file: UploadFile = File(...)):
    """Upload cover image"""
    try:
        user_repo = UserRepository(db.get_db())
        user_service = UserService(user_repo)
        return await user_service.upload_cover_image(user_id, file, storage)
    except Exception as e:
        traceback.print_exc()
        raise
