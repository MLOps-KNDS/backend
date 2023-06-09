from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas import pool_model as pool_model_schemas
from services import PoolService, ModelService, PoolModelService, get_db
from auth.jwt_bearer import JWTBearer

router = APIRouter(
    prefix="/{pool_id}/model", tags=["pool-model"], dependencies=[Depends(JWTBearer())]
)


@router.get(
    "/",
    response_model=list[pool_model_schemas.PoolModelDetailed],
    status_code=200,
)
async def get_pool_models(pool_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a list of models in a pool.

    :param db: Database session
    :param pool_id: the pool ID to retrieve models from

    :raise HTTPException: 404 status code with "Pool not found!" message
    if the specified pool ID does not exist in the database.

    :return: a list of models in the pool
    """
    if not PoolService.get_pool_by_id(db=db, id=pool_id):
        raise HTTPException(status_code=404, detail="Pool not found!")
    return PoolModelService.get_pool_models(db=db, pool_id=pool_id)


@router.put(
    "/{model_id}",
    response_model=pool_model_schemas.PoolModel,
    status_code=201,
)
async def put_pool_model(
    pool_id: int,
    model_id: int,
    pool_model_data: pool_model_schemas.PoolPutModel,
    db: Session = Depends(get_db),
):
    """
    Inserts a model into a given pool.

    :param pool_id: the pool ID to retrieve models from
    :param model_id: the model ID to retrieve from the pool
    :param pool_model_data: the information about the pool and model.
    :param db: Database session

    :raise HTTPException: 404 status code with "Pool not found!" message
    if the specified pool ID does not exist in the database.
    :raise HTTPException: 404 status code with "Model not found!" message
    if the specified model ID does not exist in the database.
    :raise HTTPException: 404 status code with "Model not found!" message
    if the specified pool ID does not exist in the database.

    :return: the newly-inserted pool record
    """
    if not PoolService.get_pool_by_id(db=db, id=pool_id):
        raise HTTPException(status_code=404, detail="Pool not found!")
    if not ModelService.get_model_by_id(db=db, model_id=model_id):
        raise HTTPException(status_code=404, detail="Model not found!")
    if PoolModelService.get_pool_model_by_model_id(db=db, id=model_id):
        raise HTTPException(
            status_code=404, detail="Model already registered in the pool!"
        )
    return PoolModelService.put_pool_model(
        db=db, pool_id=pool_id, model_id=model_id, data=pool_model_data
    )


@router.patch(
    "/{model_id}",
    response_model=pool_model_schemas.PoolModel,
    status_code=200,
)
async def patch_pool_model(
    pool_id: int,
    model_id: int,
    pool_model_data: pool_model_schemas.PoolPatchModel,
    db: Session = Depends(get_db),
):
    """
    Updates the information of an existing pool with the provided data and
    returns the updated pool information.

    :param pool_id: the pool ID to retrieve models from
    :param model_id: the model ID to retrieve from the pool
    :param pool_model_data: the information of the model in the pool to be patched.
    :param db: Database session

    :raise HTTPException: 404 status code with "Model not found in the pool!" message
    if the specified model ID does not exist in the pool database.
    :raise HTTPException: 404 status code with "Pool not found!" message
    if the specified pool ID does not exist in the database.
    :raise HTTPException: 404 status code with "Model not found!" message
    if the specified pool ID does not exist in the database.

    :return: the updated pool record
    """
    if not PoolService.get_pool_by_id(db=db, id=pool_id):
        raise HTTPException(status_code=404, detail="Pool not found!")
    if not ModelService.get_model_by_id(db=db, model_id=model_id):
        raise HTTPException(status_code=404, detail="Model not found!")
    if not PoolModelService.get_pool_model_by_model_id(db=db, id=model_id):
        raise HTTPException(status_code=404, detail="Model not found in the pool!")
    return PoolModelService.patch_pool_model(
        db=db, pool_id=pool_id, model_id=model_id, data=pool_model_data
    )


@router.delete("/{model_id}", status_code=200)
async def delete_pool_model(pool_id: int, model_id: int, db: Session = Depends(get_db)):
    """
    Deletes the pool with the given ID.

    :param pool_id: the pool ID to retrieve models from
    :param model_id: the model ID to retrieve from the pool
    :param pool_model_data: the information of the model in the pool to be deleted.
    :param db: Database session

    :raise HTTPException: 404 status code with "Pool not found!" message
    if the specified pool ID does not exist in the database.
    :raise HTTPException: 404 status code with "Model not found!" message
    if the specified pool ID does not exist in the database.
    :raise HTTPException: 404 status code with "Model not found!" message
    if the specified pool ID does not exist in the database.

    :return: a json with a "detail" key indicating success
    """
    if not PoolService.get_pool_by_id(db=db, id=pool_id):
        raise HTTPException(status_code=404, detail="Pool not found!")
    if not ModelService.get_model_by_id(db=db, model_id=model_id):
        raise HTTPException(status_code=404, detail="Model not found!")
    if not PoolModelService.get_pool_model_by_model_id(db=db, id=model_id):
        raise HTTPException(status_code=404, detail="Model not found in the pool!")
    return PoolModelService.delete_pool_model(db=db, model_id=model_id, pool_id=pool_id)
