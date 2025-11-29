from pydantic import BaseModel, Field, BeforeValidator
from typing_extensions import Annotated
from typing import List, Optional

# Helper for MongoDB ObjectId
PyObjectId = Annotated[str, BeforeValidator(str)]


class Opportunity(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    poster_id: str
    type: str
    title: str
    description: str
    requirements: List[str]
    budget: Optional[str] = None
