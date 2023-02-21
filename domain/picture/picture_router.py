import os
import secrets
import sys
from datetime import datetime

# print("------------------------------")
# print(sys.modules)
# print("------------------------------")

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session

from fastapi.responses import FileResponse, JSONResponse

# from ..ai_service.yolov3.detect_del import classification
# from ..database import get_db
# from ..
# import picture_crud
# from picture_schema import Picture
# print()
sys.path.append('/workspace')
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from database import get_db
from domain.picture import picture_crud
from models import Picture
from ai_service.food_classification.detect import classification

# from ai_service.yolov3.classification import classification

router = APIRouter(
    prefix="/api/picture",
)


# @router.get("/list", response_model=list[picture_schema.Picture])
@router.get("/list")
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

from ai_service.yolov3.code_dict import foodname
def code2name(result):
    for d in result['object']:
        d['name'] = foodname[d['name']]
    return result


@router.post('/classification')
async def upload_get_classification(file: UploadFile = File(...), db: Session = Depends(get_db)):
    import time
    st = time.time()
    try:
        os.makedirs(IMG_DIR, exist_ok=True)
        currentTime = datetime.now().strftime("%Y%m%d%H%M%S")
        saved_file_name = ''.join([currentTime, secrets.token_hex(16)])
        saved_file_name += '.jpeg'
        content = await file.read()

        file_location = os.path.join(IMG_DIR, saved_file_name)
        with open(file_location, "wb+") as file_object:
            file_object.write(content)

        picture_crud.add_picture(db=db, member_id=1, date=datetime.now(), image_name=saved_file_name)

        # get food classification
        result = classification(saved_file_name, content)
        result['fileName'] = saved_file_name
        result = code2name(result)
        result['calculation time'] = time.time() - st
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=999, detail=f"{e}")


@router.get('/images/{file_name}', response_class=FileResponse)
def get_image(file_name: str):
    result = FileResponse(''.join([IMG_DIR, file_name]))
    print(result)
    return result


# @router.get('/images/ai')
# def get_classification(file: UploadFile = File(...)):
#     content = file.read()
#     print(type(content))
#     return "---test---"
#     return JSONResponse(content=classification())


@router.delete('/images/all')
def del_image(db: Session = Depends(get_db)):
    ul = db.query(Picture)
    for u in ul:
        db.delete(u)
    db.commit()
    return True


if __name__ == "__main__":
    print(classification())
    pass