from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.models.seashells import SeaShell, Base
from app.app_config import DATABASE_URL, OFFSET, LIMIT
from app.schemas.seashells import UpdateSeaShellReq


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


def update_seashell(
    seashell_obj: SeaShell, updated_seashell: UpdateSeaShellReq, db: Session
):

    seashell_obj.collected_at = updated_seashell.collected_at
    seashell_obj.name = updated_seashell.name
    seashell_obj.species = updated_seashell.species
    seashell_obj.description = updated_seashell.description
    seashell_obj.image_url = updated_seashell.image_url

    db.commit()
    db.refresh(seashell_obj)
    return seashell_obj


def delete_seashell(seashell_obj: SeaShell, db: Session):

    db.delete(seashell_obj)
    db.commit()

    return seashell_obj
