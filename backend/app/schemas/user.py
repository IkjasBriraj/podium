from pydantic import BaseModel, Field, BeforeValidator
from typing_extensions import Annotated
from typing import List, Optional

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
