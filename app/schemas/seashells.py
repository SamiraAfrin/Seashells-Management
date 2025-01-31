from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class CreateSeaShellReq(BaseModel):
    collected_at: datetime
    name: str
    species: str
    description: Optional[str] = "No description provided"
    image_url: str


class UpdateSeaShellReq(BaseModel):
    collected_at: Optional[datetime] = None
    name: Optional[str] = None
    species: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None


class SeaShellResponse(BaseModel):
    created_at: datetime
    updated_at: datetime
    collected_at: datetime
    name: str
    species: str
    description: Optional[str]
    image_url: str

    class Config:
        from_attributes = True  # map object attributes
