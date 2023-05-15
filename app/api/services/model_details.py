from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from models import ModelDetails
from schemas.model import PutModelDetails, PatchModelDetails
from services import ModelService


class ModelDetailsService:
    @classmethod
    def get_model_details_by_id(
        cls, db: Session, model_details_id: int
    ) -> ModelDetails | None:
        """
        Retrieves a model_details from the database by it's designated id

        :param db: Database session
        :param model_details_id: id of model_details to get
        :return: model_details or None if model_details is not found
        """
        return (
            db.query(ModelDetails).filter(ModelDetails.id == model_details_id).first()
        )

    @classmethod
    def get_model_details_by_model_id(
        cls, db: Session, model_id: int
    ) -> ModelDetails | None:
        """
        Retrieves a model_details from the database by it's designated id

        :param db: Database session
        :param model_id: id of model_details to get
        :return: model_details or None if model_details is not found
        """
        return db.query(ModelDetails).filter(ModelDetails.model_id == model_id).first()

    @classmethod
    def get_model_details_by_image_tag(
        cls, db: Session, image_tag: str
    ) -> ModelDetails | None:
        """
        Retrieves a model_details from the database by it's designated id

        :param db: Database session
        :param image_tag: id of model_details to get
        :return: model_details or None if model_details is not found
        """
        return (
            db.query(ModelDetails).filter(ModelDetails.image_tag == image_tag).first()
        )

    @classmethod
    def get_models_details(
        cls, db: Session, skip: int = 0, limit: int = 100
    ) -> list[ModelDetails] | None:
        """
        Returns list of models_details with pagination

        :param db: Database session
        :param skip: how many models_details to skip
        :param limit: how many models_details to retrieve
        :return: list of retrieved models_details
        """
        models_details = db.query(ModelDetails).offset(skip).limit(limit).all()
        if len(models_details) == 0:
            return None
        return models_details

    @classmethod
    def put_model_details(
        cls, db: Session, model_details: PutModelDetails
    ) -> ModelDetails:
        """
        Creates a new model_details and adds it to the database

        :param db: Database session
        :param model_details: model_details to create
        :return: created model_details
        """
        db_model_details = ModelDetails(**model_details.dict())
        db.add(db_model_details)
        db.commit()
        db.refresh(model_details)
        ModelService.patch_model(
            db, model_details.model_id, {"model_details_id": model_details.id}
        )
        return model_details

    @classmethod
    def patch_model_details(
        cls, db: Session, model_details_id: int, model_details: PatchModelDetails
    ) -> ModelDetails | None:
        """
        Updates an existing model_details in the database

        :param db: Database session
        :param model_details_id: id of model_details to update
        :param model_details: model_details data to update
        :return: updated model_details or None if model_details is not found
        """
        db_model_details = cls.get_model_details_by_id(db, model_details_id)
        if db_model_details is None:
            return None
        for field, value in model_details:
            setattr(db_model_details, field, value)
        db.commit()
        db.refresh(db_model_details)
        return db_model_details

    @classmethod
    def delete_model_details(cls, db: Session, model_details_id: int) -> JSONResponse:
        """
        Deletes a model_details from the database

        :param db: Database session
        :param model_details_id: id of model_details to delete
        :return: JSON response with status code
        """
        model_details = cls.get_model_details_by_id(db, model_details_id)
        if model_details is None:
            return JSONResponse(
                status_code=404,
                content={
                    "message": f"ModelDetails with id {model_details_id} not found"
                },
            )
        ModelService.patch_model(db, model_details.model_id, {"model_details_id": None})
        db.delete(model_details)
        db.commit()
        return JSONResponse(status_code=204)
