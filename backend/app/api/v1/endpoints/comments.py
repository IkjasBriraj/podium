from fastapi import APIRouter, Body
from typing import List
from backend.app.schemas.post import Comment
from backend.app.db.mongodb import db
from backend.app.db.repositories.post_repository import PostRepository
from backend.app.services.post_service import PostService

router = APIRouter()


@router.post("/posts/{post_id}/like")
async def like_post(post_id: str):
    """Like a post"""
    post_repo = PostRepository(db.get_db())
    post_service = PostService(post_repo)
    return await post_service.like_post(post_id)


@router.get("/posts/{post_id}/comments", response_model=List[Comment])
async def get_comments(post_id: str):
    """Get comments for a post"""
    post_repo = PostRepository(db.get_db())
    post_service = PostService(post_repo)
    return await post_service.get_comments(post_id)


@router.post("/posts/{post_id}/comments", response_model=Comment)
async def add_comment(post_id: str, author_id: str = Body(...), content: str = Body(...)):
    """Add comment to a post"""
    post_repo = PostRepository(db.get_db())
    post_service = PostService(post_repo)
    return await post_service.add_comment(post_id, author_id, content)
