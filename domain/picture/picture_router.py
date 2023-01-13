import os
import secrets
from datetime import datetime

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
# from starlette.responses import FileResponse
from fastapi.responses import FileResponse

from database import get_db
from domain.picture import picture_schema, picture_crud
from models import Picture

from ai_service.classification import classification

router = APIRouter(
    prefix="/api/picture",
)


@router.get("/list", response_model=list[picture_schema.Picture])
def picture_list(db: Session = Depends(get_db)):
    _picture_list = picture_crud.get_picture_list(db)
    return _picture_list


# @router.post("/uploadfile/")
# def create_upload_file(file: UploadFile = File(...)):
#     return {"filename": file.filename}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, 'static/')
IMG_DIR = os.path.join(STATIC_DIR, 'images/')
SERVER_IMG_DIR = os.path.join('filestorge/', 'static/', 'images/')


@router.post('/upload-images')
async def upload_board(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        os.makedirs(IMG_DIR, exist_ok=True)
        currentTime = datetime.now().strftime("%Y%m%d%H%M%S")
        saved_file_name = ''.join([currentTime, secrets.token_hex(16)])

        content = await file.read()

        file_location = os.path.join(IMG_DIR, saved_file_name)
        with open(file_location, "wb+") as file_object:
            file_object.write(content)

        picture_crud.add_picture(db=db, member_id=1, date=datetime.now(), image_name=saved_file_name)
        result = {'fileName': saved_file_name}
        return result
    except Exception as e:
        raise HTTPException(status_code=999, detail=f"{e}")


@router.get('/images/{file_name}')
def get_image(file_name: str):
    result = FileResponse(''.join([IMG_DIR, file_name])).filename
    return result


@router.get('/images/ai/{file_name}')
def get_classification(file_name: str):
    img = ''.join([IMG_DIR, file_name])
    return classification(img)

@router.delete('/images/all')
def del_image(db: Session = Depends(get_db)):
    ul = db.query(Picture)
    for u in ul:
        db.delete(u)
    db.commit()
    return True

