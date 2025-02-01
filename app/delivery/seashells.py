from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from PIL import Image
import os
from datetime import datetime

from app.usecase.seashells import (
    get_database,
    add_seashell as add_seashell_usecase,
    get_seashell as get_seashell_usecase,
    get_all_seashells as get_all_seashells_usecase,
    update_seashell as update_seashell_usecase,
    delete_seashell as delete_seashell_usecase,
)
from app.schemas.seashells import CreateSeaShellReq, UpdateSeaShellReq, Response
from app.app_config import IMAGE_FOLDER

seashell_router = APIRouter(
    prefix="/v1/seashell", tags=["seashells"]
)  # Categorizes endpoints under "seashell"


def save_image(image: UploadFile):
    filename = image.filename

    if not os.path.exists(
        IMAGE_FOLDER
    ):  # if the folder doesn't exist, cretae the folder
        os.makedirs(IMAGE_FOLDER)

    image_path = os.path.join(IMAGE_FOLDER, filename)

    try:
        img = Image.open(image.file)
        img.verify()
        img = Image.open(image.file)  # Reopen the image to use it after verification
        img.save(image_path)
        return True, image_path
    except (IOError, SyntaxError) as e:
        return False, None


@seashell_router.post("/", response_model=Response)
def add_seashells(
    name: str = Form(...),
    collected_at: str = Form(...),
    description: str = Form(None),  # here description is optional
    species: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_database),
):

    is_image, image_url = save_image(image)
    if is_image:
        date_format = "%Y-%m-%dT%H:%M:%S"
        seashellreq = CreateSeaShellReq(
            name=name,
            collected_at=datetime.strptime(collected_at, date_format),
            species=species,
            description=description,
            image_url=image_url,
        )

        data = add_seashell_usecase(seashellreq, db)
        return Response(message="Seashell created successfully", data=data)
    else:
        raise HTTPException(status_code=400, detail="Invalid image file")


@seashell_router.get("/{seashell_id}", response_model=Response)
def get_seashell(seashell_id: int, db: Session = Depends(get_database)):

    seashell_obj = get_seashell_usecase(seashell_id, db)
    if seashell_obj is None:
        raise HTTPException(status_code=404, detail="Seashell not found")

    return Response(message="Seashell retrived successfully", data=seashell_obj)


@seashell_router.get("/", response_model=Response)
def get_all_seashells(db: Session = Depends(get_database)):

    seashell_objs = get_all_seashells_usecase(db)
    
    return Response(message="Seashells retrived successfully", data=seashell_objs)


@seashell_router.put("/{seashell_id}", response_model=Response)
def update_seashells(
    seashell_id: int,
    name: str = Form(None),
    collected_at: str = Form(None),
    description: str = Form(None),  # here description is optional
    species: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_database),
):

    seashell_obj = get_seashell_usecase(seashell_id, db)
    if seashell_obj is None:
        raise HTTPException(status_code=404, detail="Seashell not found")
    else:
        seashellreq = UpdateSeaShellReq()

        if image is not None:
            is_image, image_url = save_image(image)
            if is_image:
                seashellreq.image_url = image_url
            else:
                raise HTTPException(status_code=400, detail="Invalid image file")
        else:
            seashellreq.image_url = seashell_obj.image_url

        if collected_at is not None:
            date_format = "%Y-%m-%dT%H:%M:%S"
            seashellreq.collected_at = datetime.strptime(collected_at, date_format)
        else:
            seashellreq.collected_at = seashell_obj.collected_at

        seashellreq.name = name if name is not None else seashell_obj.name
        seashellreq.species = species if species is not None else seashell_obj.species
        seashellreq.description = (
            description if description is not None else seashell_obj.description
        )

        data = update_seashell_usecase(seashell_obj, seashellreq, db)
        return Response(message="Seashell updated successfully", data=data)


@seashell_router.delete("/{seashell_id}", response_model=Response)
def delete_seashell(seashell_id: int, db: Session = Depends(get_database)):

    seashell_obj = get_seashell_usecase(seashell_id, db)
    if seashell_obj is None:
        raise HTTPException(status_code=404, detail="Seashell not found")

    data = delete_seashell_usecase(seashell_obj, db)

    return Response(message="Seashell deleted successfully", data=data)
