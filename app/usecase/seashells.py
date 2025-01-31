from sqlalchemy.orm import Session

from app.schemas.seashells import CreateSeaShellReq, UpdateSeaShellReq
from app.models.seashells import SeaShell
from app.repository.seashells import (
    get_db,
    add_seashell as add_seashell_repo,
    get_seashell as get_seashell_repo,
    get_all_seashells as get_all_seashells_repo,
    update_seashell as update_seashell_repo,
    delete_seashell as delete_seashell_repo,
)


def get_database():
    db = next(get_db())  # Getting the session instance
    try:
        yield db
    finally:
        db.close()


def add_seashell(seashellreq: CreateSeaShellReq, db: Session):
    seashell = SeaShell(
        collected_at=seashellreq.collected_at,
        name=seashellreq.name,
        species=seashellreq.species,
        description=seashellreq.description,
        image_url=seashellreq.image_url,
    )

    return add_seashell_repo(seashell, db)


def get_seashell(seashell_id: int, db: Session):

    return get_seashell_repo(seashell_id, db)


def get_all_seashells(db: Session):

    return get_all_seashells_repo(db)


def update_seashell(
    seashell_obj: SeaShell, updated_seashellreq: UpdateSeaShellReq, db: Session
):
    return update_seashell_repo(seashell_obj, updated_seashellreq, db)


def delete_seashell(seashell_obj: SeaShell, db: Session):

    return delete_seashell_repo(seashell_obj, db)
