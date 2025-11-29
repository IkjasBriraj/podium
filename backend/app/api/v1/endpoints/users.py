from fastapi import APIRouter
from typing import List
from backend.app.schemas.user import User
from backend.app.db.mongodb import db
from backend.app.db.repositories.user_repository import UserRepository
from backend.app.services.user_service import UserService

router = APIRouter()


@router.get("/users", response_model=List[User])
async def get_users():
    """Get all users"""
    user_repo = UserRepository(db.get_db())
    user_service = UserService(user_repo)
    return await user_service.get_users()


@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    """Get user by ID"""
    user_repo = UserRepository(db.get_db())
    user_service = UserService(user_repo)
    return await user_service.get_user(user_id)
