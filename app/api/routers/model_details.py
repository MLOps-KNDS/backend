from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.model_details import ModelDetails, PutModelDetails, PatchModelDetails
from services import ModelDetailsService, get_db

router = APIRouter(prefix="/", tags=["model_details"])


@router.get("/{model_details_id}", response_model=ModelDetails, status_code=200)
async def get_model_details_by_id(model_details_id: int, db: Session = Depends(get_db)):
    """
    Retrieves the information of a specific model_details by ID.

    :param model_details_id: model_details ID
    :param db: Database session

    :raise HTTPException: 404 status code with "ModelDetails not found!" message
    if the specified gate ID does not exist in the database.

    :return: the model_details data corresponding to the given ID
    """
    model_details = ModelDetailsService.get_model_details_by_id(
        db=db, model_details_id=model_details_id
    )
    if not model_details:
        raise HTTPException(status_code=404, detail="ModelDetails not found!")
    return model_details


@router.get("/", response_model=list[ModelDetails], status_code=200)
async def get_model_details(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=0),
    db: Session = Depends(get_db),
):
    """
    Retrieves a list of model_details with pagination options (skip, limit).

    :param db: Database session
    :param skip: (optional) the number of records to skip (default: 0)
    :param limit: (optional) the maximum number of records to retrieve (default: 100)

    :raise HTTPException: 404 status code with "ModelDetails not found!" message
    if the specified range of model_details ID's does not exist in the database.

    :return: a list of model_details data, where skip < model_details_id < limit
    """
    model_details = ModelDetailsService.get_model_details(db=db, skip=skip, limit=limit)
    if not model_details:
        raise HTTPException(status_code=404, detail="ModelDetails not found!")
    return model_details


@router.put("/", response_model=ModelDetails, status_code=201)
async def put_model_details(
    model_details_data: PutModelDetails, db: Session = Depends(get_db)
):
    """
    Creates a new model_details with the given information
    and returns the model_details information.

    :param model_details_data: the information of the new model_details to be created.
    :param db: Database session

    :raise HTTPException: 400 status code with "ModelDetails already exists!" message
    if the specified model_details already exists in the database.

    :return: the model_details data corresponding to the given ID
    """
    model_details = ModelDetailsService.get_model_details_by_image_tag(
        db=db, image_tag=model_details_data.image_tag
    )
    if model_details:
        raise HTTPException(status_code=400, detail="ModelDetails already exists!")
    model_details = ModelDetailsService.put_model_details(
        db=db, model_details=model_details_data
    )
    return model_details


@router.patch("/{model_details_id}", response_model=ModelDetails, status_code=200)
async def patch_model_details(
    model_details_id: int,
    model_details_data: PatchModelDetails,
    db: Session = Depends(get_db),
):
    """
    Updates the information of an existing model_details
    and returns the model_details information.

    :param model_details_id: model_details ID
    :param model_details_data: the information of the model_details to be updated.
    :param db: Database session

    :raise HTTPException: 404 status code with "ModelDetails not found!" message
    if the specified model_details does not exist in the database.

    :return: the model_details data corresponding to the given ID
    """
    model_details = ModelDetailsService.get_model_details_by_id(
        db=db, model_details_id=model_details_id
    )
    if not model_details:
        raise HTTPException(status_code=404, detail="ModelDetails not found!")
    model_details = ModelDetailsService.get_model_details_by_image_tag(
        db=db, image_tag=model_details_data.image_tag
    )
    if model_details:
        raise HTTPException(
            status_code=400, detail="ModelDetails with the same tag already exists!"
        )
    model_details = ModelDetailsService.patch_model_details(
        db=db, model_details_id=model_details_id, model_details=model_details_data
    )
    return model_details


@router.delete("/{model_details_id}", response_model=ModelDetails, status_code=200)
async def delete_model_details(model_details_id: int, db: Session = Depends(get_db)):
    """
    Deletes a model_details from the database

    :param db: Database session
    :param model_details_id: id of model_details to delete
    :return: JSON response with status code
    """
    model_details = ModelDetailsService.get_model_details_by_id(
        db=db, model_details_id=model_details_id
    )
    if not model_details:
        raise HTTPException(status_code=404, detail="ModelDetails not found!")
    ModelDetailsService.delete_model_details(db=db, model_details_id=model_details_id)
    return model_details
