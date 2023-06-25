from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from datetime import datetime

from models import model as model_models
from models.model import ModelStatus
from schemas import model as model_schemas
from utils import ModelDeployment, ModelBuilder
from .model_details import ModelDetailsService


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
    ) -> list[model_models.Model]:
        """
        Returns list of models with pagination

        :param db: Database session
        :param skip: how many models to skip
        :param limit: how many models to retrieve
        :return: list of retrieved models
        """
        models = db.query(model_models.Model).offset(skip).limit(limit).all()
        return models

    @classmethod
    def put_model(
        cls, db: Session, model: model_schemas.ModelPut
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
        db_model.status = ModelStatus.INACTIVE
        db.add(db_model)
        db.commit()
        db.refresh(db_model)
        return db_model

    @classmethod
    def patch_model(
        cls, db: Session, model_id: int, model: model_schemas.ModelPatch
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
        cls, db: Session, model_id: int, status: ModelStatus
    ) -> model_models.Model:
        """
        Changes the status of a model in the database

        :param db: Database session
        :param model_id: id of a model to update
        :param status: new status of a model

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

        :param name: name of model to deploy
        :param model_details: model details

        :return: JSON respose indicating succesful activation
        """

        model_deployment = ModelDeployment(
            name=name,
            model_details=model_details,
        )
        model_deployment.deploy()

        return JSONResponse({"detail": "model activated"})

    @classmethod
    def deactivate_model(
        cls,
        name: str,
    ) -> JSONResponse:
        """
        Deactivates a model from a kubernetes cluster

        :param name: name of model to deactivate


        :return: JSON respose indicating succesful deactivation
        """

        ModelDeployment.delete(name)
        return JSONResponse(status_code=200, content={"detail": "model deactivated"})

    @classmethod
    def build_model(
        cls,
        db: Session,
        name: str,
        model_details: dict,
    ) -> JSONResponse:
        """
        Builds a docker image for a model and pushes it to a docker registry.

        :param name: name of model to build
        :param model_details: model details

        :return: JSON respose indicating succesful build
        """
        model_builder = ModelBuilder(
            name=name,
            mlflow_tracking_uri=model_details.mlflow_server.tracking_uri,
            artifact_uri=model_details.artifact_uri,
        )
        model_builder.build()
        image_tag = model_builder.push()

        db_model_details = ModelDetailsService.get_model_details_by_model_id(
            db, model_details.model_id
        )
        db_model_details.image_tag = image_tag
        db_model_details.updated_at = datetime.utcnow()
        db.add(db_model_details)
        db.commit()
        db.refresh(db_model_details)

        return JSONResponse(
            status_code=200,
            content={"detail": "Model image built and pushed with tag: " + image_tag},
        )
