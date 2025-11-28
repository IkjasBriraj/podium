from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Response, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel, Field, BeforeValidator
from typing_extensions import Annotated
import os
import traceback
import uuid
from backend.database import db
from backend.storage import storage

app = FastAPI(title="Sports Networking API", description="Backend for the Athlete Networking App")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Database Events ---
@app.on_event("startup")
async def startup_db_client():
    db.connect()

@app.on_event("shutdown")
async def shutdown_db_client():
    db.close()

# --- Data Models ---

# Helper for MongoDB ObjectId
PyObjectId = Annotated[str, BeforeValidator(str)]

class Skill(BaseModel):
    name: str
    endorsements: int = 0

class Experience(BaseModel):
    role: str
    org: str
    years: str
    description: Optional[str] = None

class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    role: str
    sport: str
    headline: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    category: Optional[str] = None
    profile_image: Optional[str] = None
    cover_image: Optional[str] = None
    email: Optional[str] = None
    username: Optional[str] = None
    # Sport-specific
    age: Optional[int] = None
    weight: Optional[str] = None
    height: Optional[str] = None
    playing_hand: Optional[str] = None
    years_of_experience: Optional[int] = None
    age_category: Optional[str] = None
    academy: Optional[str] = None
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
    age: Optional[int] = None
    weight: Optional[str] = None
    height: Optional[str] = None
    playing_hand: Optional[str] = None
    years_of_experience: Optional[int] = None
    age_category: Optional[str] = None
    academy: Optional[str] = None

class Post(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    author_id: str
    content: str
    media_url: Optional[str] = None
    type: str
    likes: int = 0
    comments: int = 0

class Opportunity(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    poster_id: str
    type: str
    title: str
    description: str
    requirements: List[str]
    budget: Optional[str] = None

class TrainingVideo(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str
    author: str
    description: Optional[str] = None
    video_url: str
    thumbnail_url: Optional[str] = None
    duration: Optional[str] = "00:00"
    views: Optional[str] = "0"
    type: str = "link"
    categories: List[str] = []
    analysis: Optional[List[str]] = None

# --- Helper Functions ---

def validate_media_file(file: UploadFile):
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
    return {"message": "Welcome to the Sports Networking API (MongoDB + S3)"}

@app.get("/users", response_model=List[User])
async def get_users():
    users = await db.get_db()["users"].find().to_list(1000)
    return users

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    # Try to find by custom string ID first (for legacy/migration) or ObjectId
    user = await db.get_db()["users"].find_one({"_id": user_id})
    if not user:
        # Fallback to check if it's a string id stored in a different field or just not found
        # For this app, we'll assume _id is used.
        # If using ObjectId, we might need to try converting.
        # But for simplicity, we'll stick to what's stored.
        # If we generated string IDs like "u1", they are stored as _id.
        raise HTTPException(status_code=404, detail="User not found")
    return user

# --- Profile Endpoints ---

@app.get("/profiles/{user_id}", response_model=User)
async def get_profile(user_id: str):
    user = await db.get_db()["users"].find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="Profile not found")
    return user

@app.post("/profiles", response_model=User)
async def create_profile(profile: ProfileCreateRequest):
    # Generate a simple string ID for consistency with frontend or use ObjectId
    # Using UUID string to avoid ObjectId complexity on frontend for now
    user_id = str(uuid.uuid4())
    
    new_user = profile.model_dump()
    new_user["_id"] = user_id
    new_user["profile_image"] = None
    new_user["cover_image"] = None
    new_user["skills"] = []
    new_user["experience"] = []
    # Initialize other fields
    for field in ["age", "weight", "height", "playing_hand", "years_of_experience", "age_category", "academy"]:
        new_user[field] = None

    await db.get_db()["users"].insert_one(new_user)
    return new_user

@app.put("/profiles/{user_id}", response_model=User)
async def update_profile(user_id: str, profile: ProfileUpdateRequest):
    update_data = profile.model_dump(exclude_unset=True)
    if not update_data:
         user = await db.get_db()["users"].find_one({"_id": user_id})
         if not user:
            raise HTTPException(status_code=404, detail="Profile not found")
         return user

    result = await db.get_db()["users"].update_one(
        {"_id": user_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Profile not found")
        
    user = await db.get_db()["users"].find_one({"_id": user_id})
    return user

@app.post("/profiles/{user_id}/image")
async def upload_profile_image(user_id: str, file: UploadFile = File(...)):
    validate_media_file(file)
   
    # Verify user exists
    user = await db.get_db()["users"].find_one({"_id": user_id})
    print(f"IN upload_profile_image: {user_id}, user: {user}")
    if not user:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    try:
        # Generate consistent filename so new uploads overwrite old ones
        file_extension = os.path.splitext(file.filename)[1]
        custom_filename = f"{user_id}_profile{file_extension}"
        
        # Upload to S3 with custom filename (overwrites if exists)
        image_url = storage.upload_file(file, folder="profiles", custom_filename=custom_filename)
        print(f"IN upload_profile_image: image_url: {image_url}")
        
        # Update DB
        await db.get_db()["users"].update_one(
            {"_id": user_id},
            {"$set": {"profile_image": image_url}}
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"message": "Profile image uploaded", "image_url": image_url}

@app.post("/profiles/{user_id}/cover")
async def upload_cover_image(user_id: str, file: UploadFile = File(...)):
    validate_media_file(file)
    
    user = await db.get_db()["users"].find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    try:
        # Generate consistent filename so new uploads overwrite old ones
        file_extension = os.path.splitext(file.filename)[1]
        custom_filename = f"{user_id}_cover{file_extension}"
        
        # Upload to S3 with custom filename (overwrites if exists)
        image_url = storage.upload_file(file, folder="covers", custom_filename=custom_filename)
        
        # Update DB
        await db.get_db()["users"].update_one(
            {"_id": user_id},
            {"$set": {"cover_image": image_url}}
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"message": "Cover image uploaded", "image_url": image_url}

# --- Feed and Opportunities ---

@app.get("/feed", response_model=List[Post])
async def get_feed():
    posts = await db.get_db()["posts"].find().sort("_id", -1).to_list(100)
    return posts

@app.get("/opportunities", response_model=List[Opportunity])
async def get_opportunities():
    opportunities = await db.get_db()["opportunities"].find().to_list(100)
    return opportunities

@app.post("/posts", response_model=Post)
async def create_post(
    user_id: str = Form(...),
    content: str = Form(...),
    type: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    media_url = None
    if file:
        validate_media_file(file)
        media_url = storage.upload_file(file, folder="posts")

    post_id = str(uuid.uuid4())
    new_post = {
        "_id": post_id,
        "author_id": user_id,
        "content": content,
        "media_url": media_url,
        "type": type,
        "likes": 0,
        "comments": 0
    }
    
    await db.get_db()["posts"].insert_one(new_post)
    return new_post

@app.get("/users/{user_id}/posts", response_model=List[Post])
async def get_user_posts(user_id: str):
    posts = await db.get_db()["posts"].find({"author_id": user_id}).sort("_id", -1).to_list(100)
    return posts

# --- Training Videos ---

@app.get("/training/videos", response_model=List[TrainingVideo])
async def get_training_videos(response: Response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    videos = await db.get_db()["training_videos"].find().sort("_id", -1).to_list(100)
    return videos

@app.post("/training/videos", response_model=TrainingVideo)
async def create_training_video(
    title: str = Form(...),
    author: str = Form(...),
    description: str = Form(None),
    type: str = Form(...),
    video_url: str = Form(None),
    file: Optional[UploadFile] = File(None)
):
    final_video_url = video_url
    thumbnail_url = None
    
    if type == 'file':
        if not file:
             raise HTTPException(status_code=400, detail="File is required for file upload type")
        validate_media_file(file)
        final_video_url = storage.upload_file(file, folder="training")
        thumbnail_url = None 

    elif type == 'link':
        if not video_url:
             raise HTTPException(status_code=400, detail="Video URL is required for link type")
        import re
        youtube_regex = (
            r'(https?://)?(www\.)?'
            r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
            r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
        )

        match = re.match(youtube_regex, video_url)
        if match:
            video_id = match.group(6)
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
    
    await db.get_db()["training_videos"].insert_one(new_video)
    return new_video
