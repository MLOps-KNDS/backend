"""
This module defines base service class.
It should be inherited by every other service class.

Base service class defines connection to database using sqlalchemy


Example function usage 
    def read(item: Item, db: Depends(get_db)):
        result = BaseService().read_iteam(item, db)
        return result
"""
from typing import Generator
from utils.database import SessionLocal


class BaseService:
    def get_db(self) -> Generator:
        """
        Function tries to return database session, and after variable is not used
        closes the connection.

        :return: Returns active session of database connection.
        """
        try:
            db = SessionLocal()
            yield db
        finally:
            db.close()
