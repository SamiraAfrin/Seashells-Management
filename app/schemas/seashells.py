from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class CreateSeaShellReq(BaseModel):
    collected_at: datetime
    name: str
    species: str
    description: Optional[str] = "No description provided"
    image_url: str


class SeaShellResponse(BaseModel):
    created_at: datetime
    updated_at: datetime
    collected_at: datetime
    name: str
    species: str
    description: Optional[str]
    image_url: str

    class Config:
        orm_mode = True  # Enables ORM compatibility
