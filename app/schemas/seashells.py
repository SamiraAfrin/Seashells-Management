from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import Optional


class CreateSeaShellReq(BaseModel):
    collected_at: datetime
    name: str
    species: str
    description: Optional[str] = "No description provided" 
    image_url: str


