"""
This module defines SessionLocal which may be imported for creating a
database session
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
