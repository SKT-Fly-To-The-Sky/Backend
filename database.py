from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:0000@172.16.0.169:3306/ftts?charset=utf8mb4"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:0000@jeongsuri.iptime.org:10022/ftts?charset=utf8mb4"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''
db 초기 세팅: alembic init migrations
revision 파일 생성: alembic revision --autogenerate \
revision db에 적용: alembic upgrade head

from models import Base
target_metadata = Base.metadata
'''
