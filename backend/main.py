from fastapi import FastAPI
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI(title="Sports Networking API", description="Backend for the Athlete Networking App")

# --- Data Models ---

class Skill(BaseModel):
    name: str
    endorsements: int

class Experience(BaseModel):
    role: str
    org: str
    years: str

class User(BaseModel):
    id: str
    name: str
    role: str
    sport: str
    headline: Optional[str] = None
    location: Optional[str] = None
    skills: List[Skill] = []
    experience: List[Experience] = []

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
        "location": "Kuala Lumpur, Malaysia",
        "skills": [
            {"name": "Smash", "endorsements": 45},
            {"name": "Footwork", "endorsements": 30}
        ],
        "experience": [
            {"role": "National Player", "org": "BAM", "years": "2000-2019"}
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
    return {}

@app.get("/feed", response_model=List[Post])
def get_feed():
    return posts_db

@app.get("/opportunities", response_model=List[Opportunity])
def get_opportunities():
    return opportunities_db
