from app.schemas.seashells import CreateSeaShellReq
from app.models.seashells import SeaShell
from app.repository.seashells import get_db,add_seashell as add_seashell_repo
from sqlalchemy.orm import Session

def get_database():
    db = next(get_db())  # Getting the session instance
    try:
        yield db
    finally:
        db.close()


        

def add_seashell(seashellreq: CreateSeaShellReq, db: Session):
    seashell = SeaShell(name = seashellreq.name, 
                        species = seashellreq.species,
                        description = seashellreq.description,
                        image_url = seashellreq.image_url
                        )
    
    return add_seashell_repo(seashell, db)
    


