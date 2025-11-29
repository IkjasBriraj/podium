from pydantic import BaseModel, Field, BeforeValidator
from typing_extensions import Annotated
from typing import List, Optional

# Helper for MongoDB ObjectId
PyObjectId = Annotated[str, BeforeValidator(str)]


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
