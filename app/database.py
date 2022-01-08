from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from .config import settings


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#DB Connection
# while True:
#     try:
#         conn = psycopg2.connect(dbname='fastapi', 
#         user='postgres', 
#         password='Armenia$100',
#         cursor_factory=RealDictCursor)
#         cur = conn.cursor()
#         break
#     except Exception as error:
#         print("connection to db failed")
#         print("error", error)
#         time.sleep(2)