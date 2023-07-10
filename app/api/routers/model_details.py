from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.model_details import ModelDetails, ModelDetailsPatch
from services import ModelDetailsService, get_db, MlflowServerService
from auth.jwt_bearer import JWTBearer

router = APIRouter(
    prefix="/{model_id}/details",
    tags=["model-details"],
    dependencies=[Depends(JWTBearer())],
)


@router.get("/", response_model=ModelDetails, status_code=200)
async def get_model_details_by_id(model_id: int, db: Session = Depends(get_db)):
    """
    Retrieves the information of a specific model_details by ID.

    :param model_id: model ID
    :param db: Database session

    :raise HTTPException: 404 status code with "ModelDetails not found!" message
    if the specified gate ID does not exist in the database.

    :return: the model_details data corresponding to the given ID
    """
    model_details = ModelDetailsService.get_model_details_by_model_id(
        db=db, model_id=model_id
    )
    if not model_details:
        raise HTTPException(status_code=404, detail="ModelDetails not found!")
    return model_details


@router.patch("/", response_model=ModelDetails, status_code=200)
async def patch_model_details(
    model_id: int,
    model_details_data: ModelDetailsPatch,
    db: Session = Depends(get_db),
):
    """
    Updates the information of an existing model_details
    and returns the model_details information.

    :param model_id: model ID
    :param model_details_data: the information of the model_details to be updated.
    :param db: Database session

    :raise HTTPException: 404 status code with "ModelDetails not found!" message
    if the specified model_details does not exist in the database.

    :return: the model_details data corresponding to the given ID
    """
    model_details = ModelDetailsService.get_model_details_by_model_id(
        db=db, model_id=model_id
    )
    if not model_details:
        raise HTTPException(status_code=404, detail="ModelDetails not found!")

    if model_details_data.image_tag:
        model_details = ModelDetailsService.get_model_details_by_image_tag(
            db=db, image_tag=model_details_data.image_tag
        )
        if model_details:
            raise HTTPException(
                status_code=400, detail="ModelDetails with the same tag already exists!"
            )
    if model_details_data.mlflow_server_id is not None:
        ml_flow_server = MlflowServerService.get_mlflow_server_by_id(
            db, model_details_data.mlflow_server_id
        )
        if ml_flow_server is None:
            raise HTTPException(
                status_code=400,
                detail="Mlflow server with the given ID does not exist!",
            )
    model_details = ModelDetailsService.patch_model_details(
        db=db, model_id=model_id, model_details=model_details_data
    )
    return model_details
