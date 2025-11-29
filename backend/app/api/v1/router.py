from fastapi import APIRouter
from backend.app.api.v1.endpoints import users, profiles, posts, comments, training

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(users.router, tags=["users"])
api_router.include_router(profiles.router, tags=["profiles"])
api_router.include_router(posts.router, tags=["posts"])
api_router.include_router(comments.router, tags=["comments"])
api_router.include_router(training.router, tags=["training"])
