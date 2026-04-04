from pydantic import BaseModel, Field
from typing_extensions import Annotated
from typing import Optional
from pydantic import BeforeValidator
from datetime import datetime
import uuid

# Helper for MongoDB ObjectId
PyObjectId = Annotated[str, BeforeValidator(str)]


class Post(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    author_id: str
    author_name: Optional[str] = None
    author_image: Optional[str] = None
    content: str = ""
    media_url: Optional[str] = None
    type: str
    likes: int = 0
    dislikes: int = 0
    comments: int = 0
    created_at: Optional[str] = Field(default_factory=lambda: datetime.utcnow().isoformat())


class Comment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    post_id: str
    author_id: str
    content: str
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
