from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from datetime import datetime

from models import model as model_models
from models.model import Status
from schemas import model as model_schemas
from utils import ModelDeployment


class ModelService:
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
    def get_model_by_name(cls, db: Session, name: str) -> model_models.Model | None:
        """
        Retrieves a model from the database by it's designated id

        :param db: Database session
        :param name: name of model to get
        :return: model or None if model is not found
        """
        return (
            db.query(model_models.Model).filter(model_models.Model.name == name).first()
        )

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
        models = db.query(model_models.Model).offset(skip).limit(limit).all()
        if len(models) == 0:
            return None
        return models

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
        db_model.status = Status.INACTIVE
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
    def change_model_status(
        cls, db: Session, model_id: int, status: Status
    ) -> model_models.Model:
        """
        Changes the status of a model in the database

        :param db: Database session
        :param model_id: id of a model to update
        :return: updated model
        """
        db_model = ModelService.get_model_by_id(db, model_id)
        db_model.status = status
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
        return JSONResponse({"detail": "model deleted"})

    @classmethod
    def activate_model(
        cls,
        name: str,
        model_details: dict,
    ) -> JSONResponse:
        """
        Deploys a model to a kubernetes cluster

        :param db: Database session
        :param model_id: id of model to activate

        :return: JSON respose indicating succesful activation
        """

        model_deployment = ModelDeployment(
            name=name,
            model_details={**model_details},
        )
        model_deployment.deploy()

        return JSONResponse({"detail": "model activated"})

    @classmethod
    def deactivate_model(
        cls,
        db: Session,
        model_id: int,
    ) -> JSONResponse:
        """
        Deactivates a model from a kubernetes cluster

        :param db: Database session
        :param model_id: id of model to deactivate

        :raises: HTTPException if model is already inactive
        :raises: HTTPException if model is not found

        :return: JSON respose indicating succesful deactivation
        """
        db_model = (
            db.query(model_models.Model)
            .filter(model_models.Model.id == model_id)
            .first()
        )
        if not db_model:
            raise HTTPException(status_code=404, content={"detail": "Model not found!"})
        if db_model.status == Status.INACTIVE:
            raise HTTPException(
                status_code=409, content={"detail": "Model already inactive!"}
            )

        ModelDeployment.delete(db_model.name)

        db.query(model_models.Model).filter(model_models.Model.id == model_id).update(
            {"status": Status.INACTIVE}
        )
        db.commit()
        return JSONResponse({"detail": "model deactivated"})
