from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException

from app.usecase.seashells import add_seashell as add_seashell_usecase, get_database
from app.schemas.seashells import CreateSeaShellReq
from sqlalchemy.orm import Session
from PIL import Image
import os
from datetime import datetime

seashell_router = APIRouter(prefix="/v1/seashell", tags=["seashells"])  # Categorizes endpoints under "seashell" 

def save_image(image: UploadFile):

    image_folder = "static/images/seashell_images"
    filename = image.filename

    if not os.path.exists(image_folder):  # if the folder doesn't exist, cretae the folder
        os.makedirs(image_folder)
    
    image_path = os.path.join(image_folder, filename)

    try:
        img = Image.open(image.file)
        img.verify()  
        img = Image.open(image.file)  # Reopen the image to use it after verification
        img.save(image_path)
        return True, image_path
    except (IOError, SyntaxError) as e:
        return False, None


@seashell_router.post("/")
def add_seashells(name: str = Form(...), 
    collection_at: str = Form(...),
    description: str = Form(None),  #here description is optional
    species: str = Form(...),  
    image: UploadFile = File(...),
    db: Session = Depends(get_database)):

    is_image, image_url = save_image(image)
    if is_image:
        date_format = "%Y-%m-%dT%H:%M:%S"        
        seashellreq = CreateSeaShellReq(
            name=name,
            collected_at= datetime.strptime(collection_at, date_format),
            species=species,
            description=description,
            image_url=image_url, 
        )
        return add_seashell_usecase(seashellreq, db)
    else:
        raise HTTPException(status_code=400, detail="Invalid image file")
    
