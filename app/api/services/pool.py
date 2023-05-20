"""
This module provides services which are used
to send requests directly to the database
"""

from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from fastapi.responses import JSONResponse

from schemas import pool as pool_schemas
from models import pool as pool_models


class PoolService:
    """
    Contains methods for interacting with the pool table.
    """

    @classmethod
    def get_pool_by_id(cls, db: Session, id: int) -> pool_models.Pool:
        """
        Returns the pool data found by pool id

        :param id: the pool ID to retrieve

        :return: the pool data corresponding to the given ID or None if not found
        """
        return db.query(pool_models.Pool).filter(pool_models.Pool.id == id).first()

    @classmethod
    def get_pool_by_name(cls, db: Session, name: str) -> pool_models.Pool:
        """
        Returns the pool data found by pool id

        :param id: the pool ID to retrieve

        :return: the pool data corresponding to the given ID or None if not found
        """
        return db.query(pool_models.Pool).filter(pool_models.Pool.name == name).first()

    @classmethod
    def get_pools(
        cls, db: Session, skip: int = 0, limit: int = 100
    ) -> list[pool_models.Pool] | None:
        """
        Returns a list of pool data, with optional pagination

        :param skip: (optional) the number of records to skip (default: 0)
        :param limit: (optional) the max number of records to retrieve (default: 100)

        :return: a list of pool data, where skip < user_id <= limit
        """
        pools = db.query(pool_models.Pool).offset(skip).limit(limit).all()
        print(f"pools: {pools}")
        if len(pools) == 0:
            return None
        return pools

    @classmethod
    def put_pool(cls, db: Session, pool_data: pool_schemas.PoolPut) -> pool_models.Pool:
        """
        Inserts a new pool record into the database

        :param pool_data: the user data to insert

        :return: the newly-inserted pool record
        """
        db_pool = pool_models.Pool(**pool_data.dict())
        creation_time = datetime.utcnow()
        db_pool.updated_by = db_pool.created_by
        db_pool.created_at = creation_time
        db_pool.updated_at = creation_time
        db.add(db_pool)
        db.commit()
        db.refresh(db_pool)
        return db_pool

    @classmethod
    def patch_pool(
        cls, db: Session, id: int, pool_data: pool_schemas.PoolPatch
    ) -> pool_models.Pool:
        """
        Updates an existing pool record in the database

        :param pool_data: the pool data to update

        :return: the updated pool record
        """
        db_pool = PoolService.get_pool_by_id(db=db, id=id)
        for key, value in pool_data.dict(exclude_none=True).items():
            setattr(db_pool, key, value)
        db_pool.updated_by = pool_data.updated_by
        db_pool.updated_at = datetime.utcnow()
        db.add(db_pool)
        db.commit()
        db.refresh(db_pool)
        return db_pool

    @classmethod
    def delete_pool(cls, db: Session, id: int) -> JSONResponse:
        """
        Deletes a pool record from the database

        :param id: the pool ID to delete

        :return: a json with a "detail" key indicating success
        """
        db.query(pool_models.Pool).filter(pool_models.Pool.id == id).delete()
        db.commit()
        return JSONResponse({"detail": "success"})

    @classmethod
    def get_pool_model_by_id(cls, db: Session, id: int) -> pool_models.PoolModel:
        """
        Returns the pool data found by pool id

        :param id: the pool ID to retrieve

        :return: the pool data corresponding to the given ID or None if not found
        """
        return (
            db.query(pool_models.PoolModel)
            .filter(pool_models.PoolModel.id == id)
            .first()
        )

    @classmethod
    def get_pool_models(cls, db: Session, id: int) -> list[pool_schemas.PoolModel]:
        """
        Returns a list of models from the given pool

        :param id: the pool ID to retrieve models from

        :return: a list of models belonging to the pool with the given ID
        """
        # need a fix for this, idk how to fetch models data from the database

        list_of_models = []

        models = (
            db.query(pool_models.PoolModel)
            .filter(pool_models.PoolModel.pool_id == id)
            .join(pool_models.PoolModel.model)
            .all()
        )

        for model in models:
            model_inspection = inspect(model)

            model_name = model_inspection.attrs.name.value
            model_description = model_inspection.attrs.description.value

            list_of_models.append(
                pool_schemas.PoolModel(
                    {
                        "pool_id": id,
                        "model_id": model.id,
                        "name": model_name,
                        "description": model_description,
                    }
                )
            )

        print(f"Model data: {list_of_models}")

        return list_of_models

    @classmethod
    def put_pool_model(
        cls, db: Session, data: pool_schemas.PoolPutModel
    ) -> JSONResponse:
        """
        Inserts a new model record into the pool in the database

        :param pool_data: the pool and model data to insert

        :return: a json with a "detail" key indicating success
        """
        db_pool = pool_models.PoolModel(
            pool_id=data.pool_id,
            model_id=data.model_id,
            mode=data.mode.name,
        )

        db.add(db_pool)
        db.commit()
        return JSONResponse(content={"detail": "success"})

    @classmethod
    def patch_pool_model(
        cls, db: Session, data: pool_schemas.PoolPutModel
    ) -> JSONResponse:
        """
        Inserts a new model record into the pool in the database

        :param pool_data: the pool and model data to insert

        :return: a json with a "detail" key indicating success
        """
        db_pool = (
            db.query(pool_models.PoolModel)
            .filter(data.pool_id == pool_models.PoolModel.pool_id)
            .filter(data.model_id == pool_models.PoolModel.model_id)
            .first()
        )
        for key, value in data.dict(exclude_none=True).items():
            setattr(db_pool, key, value)
        db.add(db_pool)
        db.commit()
        return JSONResponse(content={"detail": "success"})

    @classmethod
    def delete_pool_model(
        cls, db: Session, data: pool_schemas.PoolDeleteModel
    ) -> JSONResponse:
        """
        Inserts a new model record into the pool in the database

        :param data: the pool and model data to insert

        :return: a json with a "detail" key indicating success
        """
        db.query(pool_models.PoolModel).filter(
            data.pool_id == pool_models.PoolModel.pool_id
        ).delete()
        db.commit()
        return JSONResponse(content={"detail": "success"})
