import base64
import io
import json
import os
import time
from datetime import timedelta
from json import loads
from urllib.parse import urlencode

import jwt
import numpy as np
import uvicorn
from fastapi.encoders import jsonable_encoder
from jwt import PyJWTError
from fastapi import FastAPI, HTTPException, UploadFile, File, Response, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from sqlalchemy import and_, inspect, func
from sqlalchemy.orm import Session

from ai_service.yolov5.detect import classification_yolov5
from ai_service.food_volume_estimation_master.food_volume_estimation.volume_estimator import qual, quals
from ai_service.supplement_classification.supplement_classifier import sup_classification

from database import engine, Base, get_db, init_db
from PIL import Image
from io import BytesIO
from models import UserTable, ConfigTable, SupplementTable, FoodNutrientTable, \
    RecommendedNutrientTable, IntakeNutrientTable
from schema import User, Token, IntakeNutrientRequest

from datetime import datetime

Base.metadata.create_all(bind=engine)

app = FastAPI()



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
        # result = classification(content)
        result = classification_yolov5(content)
        result['object_num'] = len(result['object'])
        result['running_time'] = time.time() - st
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"error at classify \n{e}")

    try:
        qual_result = quals(content, result)
        return JSONResponse(content=qual_result)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"error at qual {e}")
