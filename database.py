from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# engine = create_engine("mysql+mysqlconnector://root:kaykay2412@localhost/ftts")
engine = create_engine("mysql+mysqlconnector://root:0000@jeongsuri.iptime.org:10012/ftts_dev?charset=utf8mb4")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

init_db()
'''
db 초기 세팅: alembic init migrations
revision 파일 생성: alembic revision --autogenerate \
revision db에 적용: alembic upgrade head

from models import Base
target_metadata = Base.metadata
'''
