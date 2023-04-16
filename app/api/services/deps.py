"""
This module provides functions for implementing Dependency Injection for API.
"""

from db.session import SessionLocal
from typing import Generator


def get_db() -> Generator:
    """
    This function creates a database session using the SessionLocal() method from
    SQLAlchemy, and yields it as a generator object.

    After lifetime of generator object ends, database session will be closed

    :return: Generator object containing the database session.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
