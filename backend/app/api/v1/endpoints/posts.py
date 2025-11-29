from fastapi import APIRouter, Form, File, UploadFile, Response
from typing import List, Optional
from backend.app.schemas.post import Post
from backend.app.schemas.opportunity import Opportunity
from backend.app.db.mongodb import db
from backend.app.db.repositories.post_repository import PostRepository
from backend.app.db.repositories.training_repository import OpportunityRepository
from backend.app.services.post_service import PostService
from backend.app.services.training_service import OpportunityService
from backend.app.infrastructure.storage import storage

router = APIRouter()


@router.get("/feed", response_model=List[Post])
async def get_feed():
    """Get feed posts"""
    post_repo = PostRepository(db.get_db())
    post_service = PostService(post_repo)
    return await post_service.get_feed()


@router.post("/posts", response_model=Post)
async def create_post(
    user_id: str = Form(...),
    content: str = Form(...),
    type: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    """Create new post"""
    post_repo = PostRepository(db.get_db())
    post_service = PostService(post_repo)
    return await post_service.create_post(user_id, content, type, file, storage)


@router.get("/users/{user_id}/posts", response_model=List[Post])
async def get_user_posts(user_id: str):
    """Get posts by user"""
    post_repo = PostRepository(db.get_db())
    post_service = PostService(post_repo)
    return await post_service.get_user_posts(user_id)


@router.get("/opportunities", response_model=List[Opportunity])
async def get_opportunities():
    """Get all opportunities"""
    opp_repo = OpportunityRepository(db.get_db())
    opp_service = OpportunityService(opp_repo)
    return await opp_service.get_opportunities()
