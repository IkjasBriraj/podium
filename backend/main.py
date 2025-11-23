from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
from pydantic import BaseModel
import os
import shutil
from pathlib import Path
import uuid

app = FastAPI(title="Sports Networking API", description="Backend for the Athlete Networking App")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Serve uploaded files as static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# --- Data Models ---

class Skill(BaseModel):
    name: str
    endorsements: int

class Experience(BaseModel):
    role: str
    org: str
    years: str
    description: Optional[str] = None

class User(BaseModel):
    id: str
    name: str
    role: str
    sport: str
    headline: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    category: Optional[str] = None  # e.g., Singles, Doubles
    profile_image: Optional[str] = None
    cover_image: Optional[str] = None
    skills: List[Skill] = []
    experience: List[Experience] = []

class ProfileCreateRequest(BaseModel):
    name: str
    role: str
    sport: str
    headline: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    category: Optional[str] = None

class ProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    headline: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    category: Optional[str] = None
    role: Optional[str] = None
    sport: Optional[str] = None

class PostCreateRequest(BaseModel):
    content: str
    type: str = "text"  # text, image, video

class Post(BaseModel):
    id: str
    author_id: str
    content: str
    media_url: Optional[str] = None
    type: str
    likes: int
    comments: int

class Opportunity(BaseModel):
    id: str
    poster_id: str
    type: str
    title: str
    description: str
    requirements: List[str]
    budget: Optional[str] = None

# --- Mock Data ---

users_db = [
    {
        "id": "u1",
        "name": "Lee Chong Wei",
        "role": "athlete",
        "sport": "Badminton",
        "headline": "3x Olympic Silver Medalist | Brand Ambassador",
        "bio": "Professional badminton player with over 20 years of experience. Former World No. 1 for 349 weeks. Passionate about developing the next generation of talent.",
        "location": "Kuala Lumpur, Malaysia",
        "category": "Singles",
        "profile_image": None,
        "cover_image": None,
        "skills": [
            {"name": "Smash", "endorsements": 45},
            {"name": "Net Play", "endorsements": 32},
            {"name": "Footwork", "endorsements": 30}
        ],
        "experience": [
            {
                "role": "National Team Player",
                "org": "Badminton Association of Malaysia (BAM)",
                "years": "2000 - 2019",
                "description": "Represented Malaysia in 4 Olympic Games. Won 3 Silver Medals."
            }
        ]
    }
]

posts_db = [
    {
        "id": "p1",
        "author_id": "u1",
        "content": "Analyzing the backhand defense today. #Badminton #Training",
        "media_url": "https://example.com/video.mp4",
        "type": "video",
        "likes": 500,
        "comments": 45
    }
]

opportunities_db = [
    {
        "id": "j1",
        "poster_id": "c1",
        "type": "sponsorship",
        "title": "Yonex Brand Ambassador 2025",
        "description": "Looking for rising stars in SE Asia.",
        "requirements": ["Top 50 National Ranking"],
        "budget": "10000 USD/year"
    }
]

# --- Helper Functions ---

def save_upload_file(upload_file: UploadFile, destination: Path):
    """Save uploaded file to destination"""
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()

def validate_media_file(file: UploadFile):
    """Validate that uploaded file is an image or video"""
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

# --- API Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Welcome to the Sports Networking API"}

@app.get("/users", response_model=List[User])
def get_users():
    return users_db

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: str):
    for user in users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# --- Profile Endpoints ---

@app.get("/profiles/{user_id}", response_model=User)
def get_profile(user_id: str):
    """Get user profile by ID"""
    for user in users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="Profile not found")

@app.post("/profiles", response_model=User)
def create_profile(profile: ProfileCreateRequest):
    """Create a new user profile"""
    # Generate unique ID
    user_id = f"u{len(users_db) + 1}"
    
    # Create new user
    new_user = {
        "id": user_id,
        "name": profile.name,
        "role": profile.role,
        "sport": profile.sport,
        "headline": profile.headline,
        "bio": profile.bio,
        "location": profile.location,
        "category": profile.category,
        "profile_image": None,
        "cover_image": None,
        "skills": [],
        "experience": []
    }
    
    users_db.append(new_user)
    return new_user

@app.put("/profiles/{user_id}", response_model=User)
def update_profile(user_id: str, profile: ProfileUpdateRequest):
    """Update existing user profile"""
    for user in users_db:
        if user["id"] == user_id:
            # Update only provided fields
            update_data = profile.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                user[key] = value
            return user
    
    raise HTTPException(status_code=404, detail="Profile not found")

@app.post("/profiles/{user_id}/image")
def upload_profile_image(user_id: str, file: UploadFile = File(...)):
    """Upload profile image"""
    # Validate file
    validate_media_file(file)
    
    # Find user
    user = None
    for u in users_db:
        if u["id"] == user_id:
            user = u
            break
    
    if not user:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    filename = f"{user_id}_profile_{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / filename
    
    # Save file
    save_upload_file(file, file_path)
    
    # Update user profile
    user["profile_image"] = f"/uploads/{filename}"
    
    return {
        "message": "Profile image uploaded successfully",
        "image_url": user["profile_image"]
    }

@app.post("/profiles/{user_id}/cover")
def upload_cover_image(user_id: str, file: UploadFile = File(...)):
    """Upload cover image"""
    # Validate file
    validate_image_file(file)
    
    # Find user
    user = None
    for u in users_db:
        if u["id"] == user_id:
            user = u
            break
    
    if not user:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    filename = f"{user_id}_cover_{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / filename
    
    # Save file
    save_upload_file(file, file_path)
    
    # Update user profile
    user["cover_image"] = f"/uploads/{filename}"
    
    return {
        "message": "Cover image uploaded successfully",
        "image_url": user["cover_image"]
    }

# --- Feed and Opportunities Endpoints ---

@app.get("/feed", response_model=List[Post])
def get_feed():
    return posts_db

@app.get("/opportunities", response_model=List[Opportunity])
def get_opportunities():
    return opportunities_db

@app.post("/posts", response_model=Post)
def create_post(
    user_id: str = Form(...),
    content: str = Form(...),
    type: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    """Create a new post with optional media"""
    
    media_url = None
    if file:
        validate_media_file(file)
        file_extension = os.path.splitext(file.filename)[1]
        filename = f"{user_id}_post_{uuid.uuid4()}{file_extension}"
        file_path = UPLOAD_DIR / filename
        save_upload_file(file, file_path)
        media_url = f"/uploads/{filename}"

    post_id = f"p{len(posts_db) + 1}"
    new_post = {
        "id": post_id,
        "author_id": user_id,
        "content": content,
        "media_url": media_url,
        "type": type,
        "likes": 0,
        "comments": 0
    }
    
    posts_db.insert(0, new_post)  # Add to top
    return new_post

@app.get("/users/{user_id}/posts", response_model=List[Post])
def get_user_posts(user_id: str):
    """Get posts for a specific user"""
    user_posts = [p for p in posts_db if p["author_id"] == user_id]
    return user_posts
