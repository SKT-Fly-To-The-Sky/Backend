import os
from datetime import timedelta
from json import loads

import jwt
import uvicorn
from jwt import PyJWTError
from fastapi import FastAPI, HTTPException, UploadFile, File, Response, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from sqlalchemy.orm import Session
from starlette import status

from ai_service.food_classification.detect import classification
from database import engine, Base, get_db, init_db
from PIL import Image
from io import BytesIO
from passlib.hash import bcrypt
from models import UserTable, FoodItemTable, ConfigTable
from schema import User, FoodItemRequest, Token

from utils.authenticate import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, SECRET_KEY, \
    ALGORITHM, oauth2_scheme, is_token_expired
from utils.log import logger
from datetime import datetime

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def handle_exception(request: Request, exc: Exception):
    logger.exception(f'request: {request}\nexecption:{exc}')
    raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/users")
async def create_user(user: User, db: Session = Depends(get_db)):
    hashed_password = bcrypt.hash(user.password)
    try:
        new_user = UserTable(userid=user.userid, hashed_password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info(f'create_user success:\n\tusername: {user.userid}, password: {user.password}\n')
        return JSONResponse(content={"message": "creating user success"}, status_code=status.HTTP_200_OK)
    except Exception as e:
        exp_msg = "Fail to Insert user to db"
        db.rollback()
        logger.exception(f"create_user fail({exp_msg}):\n{e}\n\tusername: {user.userid}, password: {user.password}\n")

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{exp_msg}")


@app.post("/login", response_model=Token)
async def login(user: User, db: Session = Depends(get_db)):
    authenticated_user = authenticate_user(db, user.userid, user.password)

    if not authenticated_user:
        logger.exception(f"login fail:\n\tusername: {user.userid}, password: {user.password}\n")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": authenticated_user.userid}, expires_delta=access_token_expires
    )

    logger.info(f'login success:\n\tusername: {user.userid}, password: {user.password}, token: {access_token}\n')

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users", response_model=User)
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if is_token_expired(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Expired token"
            )

        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Wrong token format"
            )
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong token"
        )
    user = db.query(UserTable).filter(UserTable.username == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@app.post("/food_items")
async def create_food_item(food_item: FoodItemRequest = Depends(), file: UploadFile = File(...),
                           db: Session = Depends(get_db)):
    try:
        image = await file.read()
        pil_image = Image.open(BytesIO(image))
        output = BytesIO()
        pil_image.save(output, format='JPEG')
        image_data = output.getvalue()
    except Exception as e:
        logger.exception(f"create_food_item fail:\n\t{e}\nWrong image")
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong image")

    try:
        date = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        img_name = {"userid": food_item.userid, "date": date}
        img_name = jwt.encode(img_name, SECRET_KEY, algorithm=ALGORITHM)
        food_item = FoodItemTable(img_name=img_name, userid=food_item.userid, time_div=food_item.time_div,
                                  date=date, image=image_data)
        db.add(food_item)
        db.commit()
        db.refresh(food_item)
    except Exception as e:
        logger.exception(f"create_food_item fail:\n\t{e}\nfail to save image to database")
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="fail to save image to database")

    return {"img_name": img_name}


@app.get("/food_items/{food_item_id}/image")
async def read_food_item_image(img_name: str, db: Session = Depends(get_db)):
    food_item = db.query(FoodItemTable).filter(FoodItemTable.img_name == img_name).first()

    if not food_item:
        raise HTTPException(status_code=404, detail="Food item not found")

    return Response(content=food_item.image, media_type="image/jpeg")


# app.include_router(member_router.router)
# app.include_router(picture_router.router)

@app.post('/json_data')
async def create_json_data(json_data: ConfigTable = Depends(), db: Session = Depends(get_db)):
    try:
        config_data = ConfigTable(name=json_data.name, data=json_data.data)
        db.add(config_data)
        db.commit()
        db.refresh(config_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="fail to save image to database")

    # return the newly created record
    return {"message": "config data saved successfully"}


@app.get('/json_data/{name}')
async def read_json_data(name: str, db: Session = Depends(get_db)):
    # query the database for the JsonData record with the given name
    data = db.query(ConfigTable).filter_by(name=name).first()

    # if no record was found, raise an HTTPException with a 404 status code
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='JSON data not found')

    try:
        json_data = loads(data.data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="fail to convert to json from database's data")

    # return the found record
    return JSONResponse(content=json_data)


@app.get('/classification')
async def upload_get_classification(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        content = await file.read()
        result = classification(content)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=501, detail=f"{e}")

@app.get("/error")
async def raise_error():
    1 / 0

@app.get("/init")
async def init_database():
    init_db()

#
if __name__ == "__main__":
    init_db()
    uvicorn.run(app, host="0.0.0.0", port=8000)
