from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from datetime import datetime

from models import model as model_models
from schemas import model as model_schemas


class ModelService:
    @classmethod
    def get_models(
        cls, db: Session, skip: int = 0, limit: int = 100
    ) -> list[model_models.Model] | None:
        """
        Returns list of models with pagination

        :param db: Database session
        :param skip: how many models to skip
        :param limit: how many models to retrieve
        :return: list of retrieved models
        """
        return db.query(model_models.Model).offset(skip).limit(limit).all()

    @classmethod
    def get_model_by_id(cls, db: Session, model_id: int) -> model_models.Model | None:
        """
        Retrieves a model from the database by it's designated id

        :param db: Database session
        :param model_id: id of model to get
        :return: model or None if model is not found
        """
        return (
            db.query(model_models.Model)
            .filter(model_models.Model.id == model_id)
            .first()
        )

    @classmethod
    def put_model(
        cls, db: Session, model: model_schemas.PutModel
    ) -> model_models.Model:
        """
        Creates a new model and adds it to the database

        :param db: Database sessoin
        :param model: model data to add to the database
        :return: created model
        """
        db_model = model_models.Model(**model.dict())
        creation_time = datetime.utcnow()
        db_model.updated_by = model.created_by
        db_model.created_at = creation_time
        db_model.updated_at = creation_time
        db.add(db_model)
        db.commit()
        db.refresh(db_model)
        return db_model

    @classmethod
    def patch_model(
        cls, db: Session, model_id: int, model: model_schemas.PatchModel
    ) -> model_models.Model:
        """
        Updates an existing model in the database

        :param db: Database session
        :param model_id: id of a model to update
        :param model: model data to update an existing model with
        :return: updated model
        """
        update_data = model.dict(exclude_unset=True)
        db_model = ModelService.get_model_by_id(db, model_id)
        for key, val in update_data.items():
            setattr(db_model, key, val)
        db_model.updated_by = model.updated_by
        db_model.updated_at = datetime.utcnow()
        db.add(db_model)
        db.commit()
        db.refresh(db_model)
        return db_model

    @classmethod
    def delete_model(cls, db: Session, model_id: int) -> JSONResponse:
        """
        Deletes a model from the database

        :param db: Database session
        :param model_id: id of model to delete
        :return: JSON respose indicating succesful deletion
        """
        db.query(model_models.Model).filter(model_models.Model.id == model_id).delete()
        db.commit()
        return JSONResponse({"detail": "model deleted"}, status_code=200)
