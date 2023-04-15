from fastapi import APIRouter, Query, Path, Body, HTTPException
from typing import Annotated, Optional

from ..schemas.model import Model

from ..dependencies import get_model_by_id, model_db


router = APIRouter(prefix="/api/models", tags=["models"])


class PatchModel(Model):
    """
    MLModel with all fields optional - for usage with patch request
    """

    __annotations__ = {
        field: Optional[field_type]
        for field, field_type in Model.__annotations__.items()
    }


@router.get("/")
async def get_models(skip: int = 0, limit: int = 3):
    """
    Allows retrieval of list of models from database

    :param skip: starting point to retrieve models from
    :param limit: how many models to retrieve
    :return: list of models
    """
    return list(model_db.values())[skip : skip + limit]


@router.get("/{model_id}")
async def get_single_model(model_id: Annotated[int, Path(title="id of model to get")]):
    """
    Allows retrieval of a model by it's designated id
    from database

    :param model_id: id of model to get
    :raises: HTTPException with status code 404 when
    model is not found
    :return: model
    """
    model = get_model_by_id(model_db, model_id)
    if not model:
        raise HTTPException(status_code=404, detail="model not found")
    return model


@router.patch("/{model_id}", response_model=Model)
async def update_model(
    model_id: Annotated[int, Path(title="id of model to update")],
    new_fields: Annotated[PatchModel, Body(description="fields of model to update")],
):
    """
    Allows updating a model by it's id

    :param model_id: id of model to update
    :param new_name: new name of model
    :param new_desc: new description od model
    :raises: HTTPException with status code 404 when
    model is not found
    :return: updated model
    """
    model = get_model_by_id(model_db, model_id)
    if not model:
        raise HTTPException(status_code=404, detail="model not found")
    update_data = new_fields.dict(exclude_unset=True)
    updated_model = model.copy(update=update_data)
    model_db[model_id] = updated_model
    return updated_model
