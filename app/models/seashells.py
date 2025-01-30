import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func


Base = declarative_base()


class SeaShell(Base):
    __tablename__ = "seashells"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    collected_at = Column(DateTime, nullable=False, default=func.now())
    name = Column(String)
    species = Column(String)
    description = Column(String(200), nullable=True)
    image_url = Column(String)


