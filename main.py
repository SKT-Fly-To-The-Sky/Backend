import base64
import io
import json
import os
import time
from datetime import timedelta
from json import loads
from urllib.parse import urlencode
import xmltodict
import xml.etree.ElementTree as ET


import jwt
import numpy as np
import requests
import uvicorn
from fastapi.encoders import jsonable_encoder
from jwt import PyJWTError
from fastapi import FastAPI, HTTPException, UploadFile, File, Response, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List


from sqlalchemy import and_, inspect, func
from sqlalchemy.orm import Session
from starlette import status

from ai_service.food_volume_estimation.food_volume_estimation.volume_estimator import qual, VolumeEstimator
# from ai_service.yolov3.detect_del import classification
from ai_service.yolov5.detect import classification_yolov5, classification_supplement
from database import engine, Base, get_db, init_db
from PIL import Image
from io import BytesIO
from passlib.hash import bcrypt
from db_models import UserTable, ConfigTable, SupplementTable, FoodNutrientTable, \
    RecommendedNutrientTable, IntakeNutrientTable, UserSupplementTable, FoodImageTable
from schema import User, Token, IntakeNutrientRequest

from server_utils.authenticate import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, SECRET_KEY, \
    ALGORITHM, oauth2_scheme, is_token_expired
from server_utils.log import logger
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

# db_host = os.environ['POSTGRES_HOST']
# db_port = os.environ['POSTGRES_PORT']

estimator = VolumeEstimator()


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


@app.get("/users1", response_model=User)
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
        print(e)
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
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="fail to convert to json from database's data")

    # return the found record
    return JSONResponse(content=json_data)


@app.get('/classification')
async def get_classification(userid: str, time_div: str, date: str, db: Session = Depends(get_db)):
    st = time.time()
    food_item = db.query(IntakeNutrientTable).filter(
        and_(IntakeNutrientTable.userid == userid,
             IntakeNutrientTable.time_div == time_div,
             IntakeNutrientTable.date == date)
    ).first()

    if not food_item:
        raise HTTPException(status_code=404, detail="Food item not found")

    if not food_item.image:
        raise HTTPException(status_code=404, detail="Food image not found")

    try:
        content = food_item.image
        content = np.array(Image.open(io.BytesIO(content)))
        result = classification_yolov5(content)
        result['object_num'] = len(result['object'])
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"error at classify \n{e}")
    print(result)
    try:
        # qual_result = result.copy()
        # qual_result["volumes"] = 0.790214897124221
        qual_result = qual(content, cls_results=result, estimator=estimator)
        qual_result['running_time'] = time.time() - st
        return JSONResponse(content=qual_result)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"error at qual {e}")


@app.post('/test/classification')
async def get_classification_test(file: UploadFile = File(...), db: Session = Depends(get_db)):
    st = time.time()
    try:
        image = await file.read()
        pil_image = Image.open(BytesIO(image))
        output = BytesIO()
        pil_image.save(output, format='JPEG')
        content = output.getvalue()
    except Exception as e:
        logger.exception(f"create_food_item fail:\n\t{e}\nWrong image")
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong image")

    try:
        content = np.array(Image.open(io.BytesIO(content)))
        result = classification_yolov5(content)
        # result = classification(content)
        # result["volumes"]: 0.790214897124221
        result['object_num'] = len(result['object'])
        result['running_time'] = time.time() - st
        return JSONResponse(content=result)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"error at classify \n{e}")


# @app.post('/test/volume')
# async def get_volume_test(file: UploadFile = File(...), db: Session = Depends(get_db)):
#     st = time.time()
#     try:
#         image = await file.read()
#         # pil_image = Image.open(BytesIO(image))
#         # output = BytesIO()
#         # pil_image.save(output, format='JPEG')
#         # content = output.getvalue()
#     except Exception as e:
#         logger.exception(f"create_food_item fail:\n\t{e}\nWrong image")
#         print(e)
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong image")
#
#     try:
#         print(type(image))
#         content = np.array(Image.open(io.BytesIO(image)))
#         result = qual(content)
#         result['running_time'] = time.time() - st
#         return JSONResponse(content=result)
#     except Exception as e:
#         print(e)
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"error at classify \n{e}")

@app.get("/supplements/names")
async def read_supplement_names(db: Session = Depends(get_db)):
    sup_names = db.query(SupplementTable.sup_name).all()

    if not sup_names:
        raise HTTPException(status_code=404, detail="nut names not found")

    sup_name_list = [n.sup_name for n in sup_names]

    return JSONResponse(content=sup_name_list)
    # return ["영양제 1", "영양제 2", "영양제 3"]


@app.get("/supplements/info")
async def read_supplement_info(sup_name: str, db: Session = Depends(get_db)):
    nut = db.query(SupplementTable).filter(SupplementTable.sup_name == sup_name).first()

    if not nut:
        raise HTTPException(status_code=404, detail="nut info not found")

    return JSONResponse(content=jsonable_encoder(nut))
    # return JSONResponse(contt={"kcal": 0, "protein": 0, "fat": 0, "carbo": 0, "sugar": 0, "chole": 0, "fiber": 0, "calcium": 0, "iron": 0, "magne": 0, "potass": 0, "sodium": 0, "zinc": 0, "copper": 0, "vitA": 0, "vitB1": 0, "vitB2": 0, "vitB3": 0, "vitB5": 0, "vitB6": 0, "vitB7": 0, "vitB9": 0, "vitB12": 0, "vitC": 0, "vitD": 0, "vitE": 0,"vitK": 0, "omega": 0})

@app.get("/foods/info")
async def read_food_info(food_name: str, db: Session = Depends(get_db)):
    food = db.query(FoodNutrientTable).filter(FoodNutrientTable.food_name == food_name).first()

    if not food:
        raise HTTPException(status_code=404, detail="food info not found")

    return JSONResponse(content=jsonable_encoder(food))
    # return JSONResponse(content={"food_name": "닭갈비", "serving_size": 400, "kcal": 595.61, "protein": 45.9, "fat": 25.8, "carbo": 44.9, "sugar": 21.2, "chole": 193.4, "fiber": 11.6, "calcium": 98.64, "iron": 3.38, "magne": 104.42, "potass": 1200.24, "sodium": 1535.83, "zinc": 3.55, "copper": 0.34, "vitA": 0, "vitB1": 0.24, "vitB2": 0.37, "vitB3": 1.23, "vitB5": 0, "vitB6": 0, "vitB7": 0, "vitB9": 0, "vitB12": 0, "vitC": 108.13, "vitD": 1.12, "vitE": 5.54, "vitK": 0, "omega": 0 })


@app.get("/nutrients/recommand")
async def read_recommanded_nutrient(age: str, gender: str, db: Session = Depends(get_db)):
    recommand = db.query(RecommendedNutrientTable).filter(
        and_(RecommendedNutrientTable.age == age, RecommendedNutrientTable.gender == gender)
    ).first()

    if not recommand:
        raise HTTPException(status_code=404, detail="recommanded nutrient not found")

    return JSONResponse(content=jsonable_encoder(recommand))
    # return JSONResponse(content={"age": "19~29", "gender": "M", "vitA": 3000, "vitB1": 1.2, "vitB2": 1.5, "vitB3": 16, "vitB5": 5, "vitB6": 100, "vitB7": 30, "vitB9": 1000, "vitB12": 2.4, "vitC": 2000, "vitD": 100, "vitE": 540, "vitK": 75, "omega": 210, "kcal": 2600, "protein": 65, "fat": 65, "carbo": 130, "sugar": 100, "chole": 300, "fiber": 30, "calcium": 2500, "iron": 45, "magne": 360, "potass": 3500, "sodium": 2300, "zinc": 35, "copper": 10000 })


@app.post("/{userid}/intakes/images")
async def create_intake_image(userid: str, time_div: str, date: str = None, time: str = None, file: UploadFile = File(...),
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
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        if time is None:
            time = datetime.now()

        intake = IntakeNutrientTable(userid=userid, time_div=time_div, date=date, time=time,
                                     image=image_data)
        db.add(intake)
        db.commit()
        db.refresh(intake)
    except Exception as e:
        logger.exception(f"create_food_item fail:\n\t{e}\nfail to save image to database")
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="fail to save image to database")

    return {"message": "image data saved successfully"}


@app.post("/{userid}/intakes/nutrients")
async def update_intake_nutrient(userid: str, nut_data: IntakeNutrientRequest,
                                 db: Session = Depends(get_db)):
    intake = db.query(IntakeNutrientTable).filter(
        and_(
            IntakeNutrientTable.userid == userid,
            IntakeNutrientTable.time_div == nut_data.time_div,
            IntakeNutrientTable.date == nut_data.date)
    ).first()
    if intake is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no image in that date, time-div.")
    try:
        if nut_data.date is None:
            nut_data.date = datetime.now().strftime("%Y-%m-%d")
        if nut_data.time is None:
            nut_data.time = datetime.now()

        for attr, value in vars(nut_data).items():
            if hasattr(intake, attr):
                setattr(intake, attr, value)
        # intake = IntakeNutrientTable(userid=userid, **IntakeNutrientRequest.to_dict(nut_data))
        db.commit()
        db.refresh(intake)
    except Exception as e:
        logger.exception(f"create_food_item fail:\n\t{e}\nfail to save image to database")
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="fail to save image to database")

    return {"message": "nutrient data saved successfully"}

@app.get("/{userid}/intakes/images")
async def read_intake_image(userid: str, time_div: str, date: str, db: Session = Depends(get_db)):
    query_result = db.query(IntakeNutrientTable).filter(
        and_(
            IntakeNutrientTable.userid == userid,
            IntakeNutrientTable.time_div == time_div,
            IntakeNutrientTable.date == date)
    ).first()

    if not query_result:
        raise HTTPException(status_code=404, detail="Intake not found")

    img = query_result.image

    if not img:
        raise HTTPException(status_code=404, detail="Intake img not found")

    return Response(content=img, media_type="image/jpeg")


@app.get("/{userid}/intakes/nutrients/time-div")
async def read_intake_nutrient_time_dev(userid: str, time_div: str, date: str, db: Session = Depends(get_db)):
    nutrients = db.query(IntakeNutrientTable).filter(
        and_(
            IntakeNutrientTable.userid == userid,
            IntakeNutrientTable.time_div == time_div,
            IntakeNutrientTable.date == date)
    ).first()

    if not nutrients:
        raise HTTPException(status_code=404, detail="Intake nutrients not found")

    nutrients.image = None

    return JSONResponse(content=jsonable_encoder(nutrients))

@app.get("/{userid}/supplements/list")
async def read_supplement_list(userid: str, db: Session = Depends(get_db)):
    supplement_models = db.query(UserTable).filter(UserTable.userid == userid).first().supplements

    if not supplement_models:
        raise HTTPException(status_code=404, detail="supplements not found")

    supplements = [getattr(row, "sup_name") for row in supplement_models]

    return JSONResponse(content=jsonable_encoder(supplements))

@app.get("/{userid}/foods/recommand")
async def food_recommand(userid: str, time_div: str, db: Session = Depends(get_db)):
    # nutrients = db.query(FoodImageTable).filter(
    #     and_(
    #         FoodImageTable.food_name == food_name,
    #         )
    # ).first()
    #
    # if not nutrients:
    #     raise HTTPException(status_code=404, detail="Intake nutrients not found")
    #
    # nutrients.image = None
    # return JSONResponse(content=jsonable_encoder(nutrients))

    data = [
        {"name": "김밥", "image": "https://dl.dropbox.com/s/f2e96zkk9abela8/%EA%B9%80%EB%B0%A5.jpeg?dl=0"},
        {"name": "김치찌개", "image": "https://dl.dropbox.com/s/cwxyldl5buwg834/%EA%B9%80%EC%B9%98%EC%B0%8C%EA%B0%9C.jpeg?dl=0"},
        {"name": "닭발", "image": "https://dl.dropbox.com/s/wltnsii4rk29aho/%EB%8B%AD%EB%B0%9C.jpeg?dl=0"},
        {"name": "돈까스", "image": "https://dl.dropbox.com/s/3gh0r4syqy8snew/%EB%8F%88%EA%B9%8C%EC%8A%A4.jpeg?dl=0"},
        {"name": "떡볶이", "image": "https://dl.dropbox.com/s/5gz3anhtd7ewzjb/%EB%96%A1%EB%B3%B6%EC%9D%B4.jpeg?dl=0"},
        {"name": "사과", "image": "https://dl.dropbox.com/s/pyyn6ix529ihesh/%EC%82%AC%EA%B3%BC.jpeg?dl=0"},
        {"name": "삼겹살구이", "image": "https://dl.dropbox.com/s/hp9mgokkfhoz6w3/%EC%82%BC%EA%B2%B9%EC%82%B4.jpeg?dl=0"},
        {"name": "삼계탕", "image": "https://dl.dropbox.com/s/72o11r0fp1fy38d/%EC%82%BC%EA%B3%84%ED%83%95.jpeg?dl=0"},
        {"name": "샐러드", "image": "https://dl.dropbox.com/s/w8c35mfyo545sxt/%EC%83%90%EB%9F%AC%EB%93%9C.jpeg?dl=0"},
        {"name": "순대국", "image": "https://dl.dropbox.com/s/qc02fmlasrwzvm6/%EC%88%9C%EB%8C%80%EA%B5%AD.jpeg?dl=0"},
        {"name": "제육덮밥", "image": "https://dl.dropbox.com/s/z39bmy08ll7an62/%EC%A0%9C%EC%9C%A1%EB%8D%AE%EB%B0%A5.jpeg?dl=0"},
        {"name": "짜장면", "image": "https://dl.dropbox.com/s/1so11apa7uvqs3p/%EC%A7%9C%EC%9E%A5%EB%A9%B4.jpeg?dl=0"},
        {"name": "치킨", "image": "https://dl.dropbox.com/s/6t8qsilk9jjguc1/%EC%B9%98%ED%82%A8.jpeg?dl=0"},
        {"name": "카레", "image": "https://dl.dropbox.com/s/h1gwprs985vv5ko/%EC%B9%B4%EB%A0%88.jpeg?dl=0"},
        {"name": "피자", "image": "https://dl.dropbox.com/s/c8eh34g4elnqpdq/%ED%94%BC%EC%9E%90.jpeg?dl=0"},
        {"name": "햄버거", "image": "https://dl.dropbox.com/s/rcmwvkl8sjdwfnb/%ED%96%84%EB%B2%84%EA%B1%B0.jpeg?dl=0"},
        {"name": "샌드위치", "image": "https://dl.dropbox.com/s/n8elmgqne4m5vbi/%EC%83%8C%EB%93%9C%EC%9C%84%EC%B9%98.jpeg?dl=0"},
        {"name": "라면", "image": "https://dl.dropbox.com/s/kdbdhuo47cdfhi7/%EB%9D%BC%EB%A9%B4.jpeg?dl=0"},
        {"name": "된장찌개", "image": "https://dl.dropbox.com/s/pl7kcss1101ujmx/%EB%90%9C%EC%9E%A5%EC%B0%8C%EA%B0%9C.jpeg?dl=0"},
        {"name": "토스트", "image": "https://dl.dropbox.com/s/17q0vm86y4njnjc/%ED%86%A0%EC%8A%A4%ED%8A%B8.jpeg?dl=0"},
        {"name": "족발", "image": "https://dl.dropbox.com/s/fou6vgvsmt2uff5/%EC%A1%B1%EB%B0%9C.jpeg?dl=0"},
        {"name": "가츠동", "image": "https://dl.dropbox.com/s/t7mymx9lo5sn01e/%EA%B0%80%EC%B8%A0%EB%8F%99.jpeg?dl=0"},
        {"name": "햄치즈샌드위치", "image": "https://dl.dropbox.com/s/kioahfs7v432i60/%ED%96%84%EC%B9%98%EC%A6%88%EC%83%8C%EB%93%9C%EC%9C%84%EC%B9%98.jpeg?dl=0"},
        {"name": "연어샐러드", "image": "https://dl.dropbox.com/s/qsxxawyze2a8xi8/%EC%97%B0%EC%96%B4%EC%83%90%EB%9F%AC%EB%93%9C.jpeg?dl=0"},
        {"name": "새우볶음밥", "image": "https://dl.dropbox.com/s/zvhpi4f7hthegac/%EC%83%88%EC%9A%B0%EB%B3%B6%EC%9D%8C%EB%B0%A5.jpeg?dl=0"},
        {"name": "해물덮밥", "image": "https://dl.dropbox.com/s/1e9edgfqvki1eld/%ED%95%B4%EB%AC%BC%EB%8D%AE%EB%B0%A5.jpeg?dl=0"},
        {"name": "훈제오리", "image": "https://dl.dropbox.com/s/r64sgvnlthgdbnx/%ED%9B%88%EC%A0%9C%EC%98%A4%EB%A6%AC.jpeg?dl=0"},
        {"name": "우동", "image": "https://dl.dropbox.com/s/ypwnuan9kab5g2a/%EC%9A%B0%EB%8F%99.jpeg?dl=0"}
    ]

    recommand_list = []
    result = []

    if time_div == '아침' or time_div == 'morning':
        recommand_list += ["사과", "햄치즈샌드위치", "연어샐러드"]
    elif time_div == "점심" or time_div == "lunch":
        recommand_list += ["삼계탕", "새우볶음밥", "해물덮밥"]
    elif time_div == "저녁" or time_div == "dinner":
        recommand_list += ["삼겹살구이", "훈제오리", "우동"]

    for d in data:
        if d.get("name") in recommand_list:
            result.append(d)

    return JSONResponse(content=result)

@app.get("/{userid}/intakes/nutrients/day")
async def read_intake_nutrient_day(userid: str, date: str, db: Session = Depends(get_db)):
    nutrients = db.query(IntakeNutrientTable).filter(
        and_(
            IntakeNutrientTable.userid == userid,
            IntakeNutrientTable.date == date)
    ).all()

    if not nutrients:
        raise HTTPException(status_code=404, detail="Intake nutrients not found")

    nut_sum = {}
    columns = [c.name for c in inspect(IntakeNutrientTable).c if c.name != 'id']
    not_sum_list = ['userid', 'date']
    not_include_list = ['time', 'time_div', 'image']
    # Use a list comprehension to construct a list of sum functions for each column
    # Use SQLAlchemy's query function to calculate the total for each column
    for nutrient in nutrients:
        for column in columns:
            if column in not_include_list:
                continue
            if getattr(nutrient, column) is None:
                nut_sum[column] = 0
                continue
            if column not in nut_sum or column in not_sum_list:
                nut_sum[column] = getattr(nutrient, column)
            else:
                nut_sum[column] += getattr(nutrient, column)

    # Create a new instance of the model with the column sums
    # new_instance = IntakeNutrientTable(**nut_sum)
    # print(nut_sum)
    return {"result": nut_sum}
    # return JSONResponse(content=json.dumps(nut_sum))

@app.get("/{userid}/supplements/recommand")
async def read_recommanded_supplement(userid: str, db: Session = Depends(get_db)):
    # img = db.query(IntakeNutrientTable).filter(
    #     and_(
    #         IntakeNutrientTable.userid == userid,
    #         IntakeNutrientTable.time_div == 'testt',
    #         IntakeNutrientTable.date == '2023-02-21')
    # ).first().image
    # encoded_image = base64.b64encode(img).decode('utf-8')

    sup_list = ["힐링팩토리 블루마린 오메가3", "헬스프랜드 캐나다 슈퍼징코플러스"]
    data = []
    for sup in sup_list:
        data_dict = {}
        url = f"http://openapi.11st.co.kr/openapi/OpenApiService.tmall?key=37d58531ff7cd34e93ba18123f509497&apiCode=ProductSearch&keyword={sup}&option=Categories"
        response = requests.get(url)
        xml_data = response.content.decode('EUC-KR')

        xml_dict = xmltodict.parse(xml_data)
        data_dict['name'] = xml_dict['ProductSearchResponse']['Products']['Product'][0]['ProductName']
        data_dict['image'] = xml_dict['ProductSearchResponse']['Products']['Product'][0]['ProductImage']
        data_dict['link'] = xml_dict['ProductSearchResponse']['Products']['Product'][0]['DetailPageUrl']
        data.append(data_dict)
        # return JSONResponse(content=xml_dict)
    return JSONResponse(content=data)


@app.post("/supplements/classification")
async def read_supplements_classification(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        image = await file.read()
        pil_image = Image.open(BytesIO(image))
        output = BytesIO()
        pil_image.save(output, format='JPEG')
        image_data = output.getvalue()
        image_data = np.array(Image.open(io.BytesIO(image_data)))
    except Exception as e:
        logger.exception(f"create_food_item fail:\n\t{e}\nWrong image")
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong image")



    return JSONResponse(content=classification_supplement(image_data))
    # return Response(content=, media_type="image/jpeg")


@app.post("/{userid}/supplements")
async def add_supplement(userid: str, supplement_name: str, db: Session = Depends(get_db)):
    try:
        new_sup = UserSupplementTable(userid=userid, sup_name=supplement_name)
        db.add(new_sup)
        db.commit()
        db.refresh(new_sup)
        return JSONResponse(content={"message": "add supplement success"}, status_code=status.HTTP_200_OK)
    except Exception as e:
        exp_msg = "Fail to Insert supplement to db"
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{exp_msg}")


@app.get("/error")
async def raise_error():
    1 / 0


@app.get("/init")
async def init_database():
    init_db()

if __name__ == "__main__":
    import subprocess
    def kill_server(port=8000):
        try:
            cmd = f"lsof -i :{port}"
            pid = subprocess.check_output(cmd.split()).decode().split()[10]
            print(pid)
            cmd = f"kill {pid}"
            subprocess.call(cmd.split())
            time.sleep(1)
        except subprocess.CalledProcessError:
            pass


    kill_server(port=8000)

    init_db()
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # subprocess.call("uvicorn main:app --reload")

# curl -L -o ./ai_service/yolov3/weights/best_403food_e200b150v2.pt https://www.dropbox.com/s/msz9yfrmsrs0zst/best_403food_e200b150v2.pt?dl=0
# curl -L -o ./ai_service/food_volume_estimation_master/food_volume_estimation/monovideo_fine_tune_food_videos.h5 https://www.dropbox.com/s/zqo3qfzoy7b9spp/monovideo_fine_tune_food_videos.h5?dl=0
# curl -L -o ./ai_service/food_volume_estimation_master/food_volume_estimation/mask_rcnn_food_segmentation.h5 https://www.dropbox.com/s/uewabex707xh2n0/mask_rcnn_food_segmentation.h5?dl=0
# uvicorn main:app --reload