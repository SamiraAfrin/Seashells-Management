from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from fastapi import Depends

from app.models.seashells import SeaShell, Base
from app.app_config import DATABASE_URL, OFFSET, LIMIT


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


def get_seashell(seashell_id: int, db: Session):
    seashell_obj = db.query(SeaShell).filter(SeaShell.id == seashell_id).first()

    return seashell_obj


def get_all_seashells(db: Session):
    sea_shells = db.query(SeaShell).offset(OFFSET).limit(LIMIT).all()

    return sea_shells
