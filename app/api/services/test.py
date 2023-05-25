"""
This module provides services which are used
to send requests directly to the database
"""

from datetime import datetime
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from schemas import test as test_schemas
from models import test as test_models


class TestService:
    @classmethod
    def get_test_by_id(cls, db: Session, id: int) -> test_models.Test | None:
        """
        Returns the test data found by test id

        :param id: the test ID to retrieve

        :return: the test data corresponding to the given ID or None if not found
        """
        return db.query(test_models.Test).filter(test_models.Test.id == id).first()

    @classmethod
    def get_test_by_name(cls, db: Session, name: str) -> test_models.Test | None:
        """
        Returns the test data found by test id

        :param id: the test ID to retrieve

        :return: the test data corresponding to the given ID or None if not found
        """
        return db.query(test_models.Test).filter(test_models.Test.name == name).first()

    @classmethod
    def get_tests(
        cls, db: Session, skip: int = 0, limit: int = 100
    ) -> list[test_models.Test]:
        """
        Returns a list of test data, with optional pagination

        :param skip: (optional) the number of records to skip (default: 0)
        :param limit: (optional) the max number of records to retrieve (default: 100)

        :return: a list of test data, where skip < test_id <= skip+limit
        """
        tests = db.query(test_models.Test).offset(skip).limit(limit).all()
        return tests

    @classmethod
    def put_test(cls, db: Session, test_data: test_schemas.TestPut) -> test_models.Test:
        """
        Inserts a new test record into the database

        :param test_data: the user data to insert

        :return: the newly-inserted test record
        """
        db_test = test_models.Test(**test_data.dict())
        creation_time = datetime.utcnow()
        db_test.updated_by = db_test.created_by
        db_test.created_at = creation_time
        db_test.updated_at = creation_time
        db.add(db_test)
        db.commit()
        db.refresh(db_test)
        return db_test

    @classmethod
    def patch_test(
        cls, db: Session, id: int, test_data: test_schemas.TestPatch
    ) -> test_models.Test:
        """
        Updates an existing test record in the database

        :param test_data: the test data to update

        :return: the updated test record
        """
        db_test = TestService.get_test_by_id(db=db, id=id)
        for key, value in test_data.dict(exclude_none=True).items():
            setattr(db_test, key, value)
        db_test.updated_by = test_data.updated_by
        db_test.updated_at = datetime.utcnow()
        db.add(db_test)
        db.commit()
        db.refresh(db_test)
        return db_test

    @classmethod
    def delete_test(cls, db: Session, id: int) -> JSONResponse:
        """
        Deletes a test record from the database

        :param id: the test ID to delete

        :return: a json with a "detail" key indicating success
        """
        db.query(test_models.Test).filter(test_models.Test.id == id).delete()
        db.commit()
        return JSONResponse({"detail": "success"})
