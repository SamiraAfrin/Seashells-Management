from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from fastapi import Depends

from app.models.seashells import SeaShell, Base


DATABASE_URL = "sqlite:///./seashell.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def add_seashell(seashell: SeaShell, db: Session):
    db.add(seashell)
    db.commit()
    db.refresh(seashell) 
    return seashell
