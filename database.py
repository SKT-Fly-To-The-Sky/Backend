from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:0000@host.docker.internal:3306/ftts?charset=utf8mb4"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:0000@172.23.240.72:3306/ftts?charset=utf8mb4"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://connectuser:0000@127.0.0.1:3306/ftts?charset=utf8mb4"

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
