from fastapi import APIRouter, Path, Query
from fastapi.responses import JSONResponse
from typing import List, Annotated

from api.schemas.test import Test
from api.utils.utility_functions import test_db, get_model_by_id


router = APIRouter(prefix="/api/tests", tags=["tests"])


@router.get("/")
async def get_tests(
    skip: Annotated[int, Query(ge=0)] = 0, limit: Annotated[int, Query(ge=0)] = 3
) -> List[Test]:
    """
    Allows retrieval of list of tests from database

    :param skip: starting point to retrieve tests from
    :param limit: how many tests to retrieve
    :return: list of tests
    """
    return list(test_db.values())[skip : skip + limit]


@router.get("/{test_id}")
async def get_test_by_id(test_id: Annotated[int, Path(title="id of model to get")]):
    """
    Allows retrieval of a test by it's designated id
    from database

    :param test_id: id of test to get
    :raises: HTTPException with status code 404 when
    test is not found
    :return: test
    """
    test = get_model_by_id(test_db, test_id)
    if not test:
        return JSONResponse(status_code=404, content={"message": "test not found"})
    return test
