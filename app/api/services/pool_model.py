from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from schemas import pool_model as pool_model_schemas
from models import pool as pool_model_models


class PoolModelService:
    @classmethod
    def get_pool_model_by_model_id(
        cls, db: Session, id: int
    ) -> pool_model_models.PoolModel:
        """
        Returns the pool data found by pool id

        :param id: the pool ID to retrieve

        :return: the pool data corresponding to the given ID or None if not found
        """
        return (
            db.query(pool_model_models.PoolModel)
            .filter(pool_model_models.PoolModel.model_id == id)
            .first()
        )

    @classmethod
    def get_pool_models(
        cls, db: Session, pool_id: int
    ) -> list[pool_model_schemas.PoolModelDetailed]:
        """
        Returns a list of models from the given pool

        :param pool_id: the pool ID to retrieve models from

        :return: a list of more detailed models belonging to the pool with the given ID
        """

        pool_data = (
            db.query(pool_model_models.PoolModel)
            .filter(pool_model_models.PoolModel.pool_id == pool_id)
            .all()
        )

        list_of_models = [
            pool_model_schemas.PoolModelDetailed(
                model_id=pool_model.model_id,
                pool_id=pool_id,
                name=pool_model.model.name,
                description=pool_model.model.description,
                mode=pool_model.mode,
                weight=pool_model.weight,
            )
            for pool_model in pool_data
        ]

        return list_of_models

    @classmethod
    def put_pool_model(
        cls,
        db: Session,
        pool_id: int,
        model_id: int,
        data: pool_model_schemas.PoolPutModel,
    ) -> JSONResponse:
        """
        Inserts a new model record into the pool in the database

        :param pool_id: the pool ID to retrieve models from
        :param model_id: the model ID to retrieve from the pool
        :param data: the pool and model data to insert

        :return: a json with a "detail" key indicating success
        """
        db_pool = pool_model_models.PoolModel(
            pool_id=pool_id,
            model_id=model_id,
            **data.dict(exclude_none=True),
        )

        db.add(db_pool)
        db.commit()
        db.refresh(db_pool)
        return db_pool

    @classmethod
    def patch_pool_model(
        cls,
        db: Session,
        pool_id: int,
        model_id: int,
        data: pool_model_schemas.PoolPatchModel,
    ) -> JSONResponse:
        """
        Inserts a new model record into the pool in the database

        :param pool_id: the pool ID to retrieve models from
        :param model_id: the model ID to retrieve from the pool
        :param data: the pool and model data to patch

        :return: a json with a "detail" key indicating success
        """
        db_pool_model = (
            db.query(pool_model_models.PoolModel)
            .filter(pool_model_models.PoolModel.pool_id == pool_id)
            .filter(pool_model_models.PoolModel.model_id == model_id)
            .first()
        )
        for key, value in data.dict(exclude_none=True).items():
            setattr(db_pool_model, key, value)
        db.add(db_pool_model)
        db.commit()
        db.refresh(db_pool_model)
        return db_pool_model

    @classmethod
    def delete_pool_model(
        cls, db: Session, model_id: int, pool_id: int
    ) -> JSONResponse:
        """
        Inserts a new model record into the pool in the database

        :param pool_id: the pool ID to retrieve models from
        :param model_id: the model ID to retrieve from the pool

        :return: a json with a "detail" key indicating success
        """
        db.query(pool_model_models.PoolModel).filter(
            pool_model_models.PoolModel.pool_id == pool_id
        ).filter(pool_model_models.PoolModel.model_id == model_id).delete()
        db.commit()
        return JSONResponse(content={"detail": "success"})
