from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from services import TestService, get_db
from models import Test as test_model
from schemas import test as test_schema


router = APIRouter("/test", tags=["test"])


@router.get("/")
async def get_tests(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[test_model]:
    """
    Retrieves a list of tests with pagination options (skip, limit).

    :param db: Database session
    :param skip: (optional) the number of records to skip (default: 0)
    :param limit: (optional) the maximum number of records to retrieve (default: 100)

    :return: a list of user data, where skip < test_id < limit
    """
    tests = TestService.get_tests(db=db, skip=skip, limit=limit)
    return tests


@router.get("/{test_id}", response_model=test_schema.Test)
async def get_test(test_id: int, db: Session = Depends(get_db)) -> test_model:
    """
    Retrieves the information of a specific test by ID.

    :param test_id: test ID
    :param db: Database session

    :return: the test data corresponding to the given ID

    :raise HTTPException: 404 status code with "Test not found!" message
    if the specified test ID does not exist in the database.
    """
    test = TestService.get_test_by_id(db=db, id=test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found!")
    return test


@router.put("/", response_model=test_schema.Test)
async def put_test(
    test_data: test_schema.TestPut, db: Session = Depends(get_db)
) -> test_model:
    """
    Creates a new test with the given information and returns the test information.

    :param test_data: the information of the new test to be created.
    :param db: Database session

    :return: the newly-inserted test record

    :raise HTTPException: 400 status code with "Name already registered"
    message if the provided name already exists in the database.
    """
    if TestService.get_test_by_name(db=db, name=test_data.name):
        raise HTTPException(status_code=400, detail="Name already registered")
    return TestService.put_test(db=db, test_data=test_data)


@router.delete("/{test_id}", response_model=test_schema.Test)
async def delete_test(test_id: int, db: Session = Depends(get_db)) -> test_model:
    """
    Deletes a test with the given ID and returns the test information.

    :param test_id: test ID
    :param db: Database session

    :return: the deleted test record

    :raise HTTPException: 404 status code with "Test not found!" message
    if the specified test ID does not exist in the database.
    """
    test = TestService.get_test_by_id(db=db, id=test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found!")
    return TestService.delete_test(db=db, test=test)


@router.patch("/{test_id}", response_model=test_schema.Test)
async def patch_test(
    test_id: int, test_data: test_schema.TestPatch, db: Session = Depends(get_db)
) -> test_model:
    """
    Updates a test with the given information and returns the test information.

    :param test_id: test ID
    :param test_data: the information of the test to be updated.
    :param db: Database session

    :return: the updated test record

    :raise HTTPException: 404 status code with "Test not found!" message
    if the specified test ID does not exist in the database.
    """
    test = TestService.get_test_by_id(db=db, id=test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found!")
    return TestService.patch_test(db=db, test=test, test_data=test_data)
