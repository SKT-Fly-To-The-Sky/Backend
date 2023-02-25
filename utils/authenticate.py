from datetime import timedelta, datetime

import jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import database
from models import UserTable

# JWT configuration
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(UserTable).filter(UserTable.userid == username).first()
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def is_token_expired(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    expire = datetime.fromtimestamp(payload['exp'])
    if datetime.utcnow() >= expire:
        return True
    else:
        return False
