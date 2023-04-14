"""
This module defines our database connection and Base class using SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


def get_db_link() -> str:
    USER = os.environ.get("POSTGRES_USER")
    PASS = os.environ.get("POSTGRES_PASSWORD")
    DB = os.environ.get("POSTGRES_DB")
    HOST = os.environ.get("POSTGRES_HOST")
    SQLALCHEMY_DATABASE_URL = f"postgresql://{USER}:{PASS}@{HOST}/{DB}"
    return SQLALCHEMY_DATABASE_URL


engine = create_engine(get_db_link(), pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
