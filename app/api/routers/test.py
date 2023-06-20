"""
This module contains the API routes and their corresponding
functions for handling test-related requests.
"""

from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas import test as test_schema
from services import TestService, get_db
from auth.jwt_bearer import JWTBearer


router = APIRouter(prefix="/test", tags=["test"], dependencies=[Depends(JWTBearer())])


@router.get("/{test_id}", response_model=test_schema.Test, status_code=200)
async def get_test(test_id: int, db: Session = Depends(get_db)):
    """
    Retrieves the information of a specific test by ID.

    :param test_id: test ID
    :param db: Database session

    :raise HTTPException: 404 status code with "Test not found!" message
    if the specified test ID does not exist in the database.

    :return: the test data corresponding to the given ID
    """
    test = TestService.get_test_by_id(db=db, id=test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found!")
    return test


@router.get("/", response_model=list[test_schema.Test], status_code=200)
async def get_tests(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=0),
    db: Session = Depends(get_db),
):
    """
    Retrieves a list of tests with pagination options (skip, limit).

    :param db: Database session
    :param skip: (optional) the number of records to skip (default: 0)
    :param limit: (optional) the maximum number of records to retrieve (default: 100)

    :raise HTTPException: 404 status code with "Test not found!" message
    if the specified range of test ID's does not exist in the database.

    :return: a list of user data, where skip < test_id < limit
    """
    tests = TestService.get_tests(db=db, skip=skip, limit=limit)
    return tests


@router.put("/", response_model=test_schema.Test, status_code=201)
async def put_test(test_data: test_schema.TestPut, db: Session = Depends(get_db)):
    """
    Creates a new test with the given information and returns the test information.

    :param test_data: the information of the new test to be created.
    :param db: Database session

    :raise HTTPException: 409 status code with "Name already registered"
    message if the provided name already exists in the database.

    :return: the newly-inserted test record
    """
    if TestService.get_test_by_name(db=db, name=test_data.name):
        raise HTTPException(status_code=409, detail="Name already registered")
    return TestService.put_test(db=db, test_data=test_data)


@router.patch("/{test_id}", response_model=test_schema.Test, status_code=200)
async def patch_test(
    test_id: int, test_data: test_schema.TestPatch, db: Session = Depends(get_db)
):
    """
    Updates a test with the given information and returns the test information.

    :param test_id: test ID
    :param test_data: the information of the test to be updated.
    :param db: Database session

    :raise HTTPException: 404 status code with "Test not found!" message
    if the specified test ID does not exist in the database.
    :raise HTTPException: 409 status code with "Name already registered"
    message if the provided name already exists in the database.

    :return: the updated test record
    """
    if not TestService.get_test_by_id(db=db, id=test_id):
        raise HTTPException(status_code=404, detail="Test not found!")
    if TestService.get_test_by_name(db=db, name=test_data.name):
        raise HTTPException(status_code=409, detail="Name already registered")
    return TestService.patch_test(db=db, id=test_id, test_data=test_data)


@router.delete("/{test_id}", status_code=200)
async def delete_test(test_id: int, db: Session = Depends(get_db)):
    """
    Deletes a test with the given ID and returns the test information.

    :param test_id: test ID
    :param db: Database session

    :raise HTTPException: 404 status code with "Test not found!" message
    if the specified test ID does not exist in the database.

    :return: the deleted test record
    """
    test = TestService.get_test_by_id(db=db, id=test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found!")
    return TestService.delete_test(db=db, id=test_id)
