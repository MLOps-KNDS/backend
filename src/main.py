"""
This is the main module.

It contains the FastAPI app.
"""

from fastapi import FastAPI, Query
from typing import Optional, Annotated
from schemas.models import Model

app = FastAPI()

models = {
    1: Model(id=1, name="Model 1"),
    2: Model(id=2, name="Model 2", description="This is a description"),
    3: Model(id=3, name="Model 3"),
    4: Model(id=4, name="Model 4"),
    5: Model(id=5, name="Model 5"),
    6: Model(id=6, name="Model 6"),
    7: Model(id=7, name="Model 7"),
    8: Model(id=8, name="Model 8", description="Very nice model"),
    9: Model(id=9, name="Model 9"),
    10: Model(id=10, name="Model 10"),
}

@app.get("/models/")
async def get_models(skip: Optional[int] = 0, 
                     limit: Optional[int] = 5):
    """
    Endpoint to retrieve a list of models.

    :param skip: The number of models to skip in the list.
    :param limit: The maximum number of models to return.
    :return: A list of models.
    """
    return list(models.values())[skip:skip + limit]

@app.get("/models/{model_id}")
async def get_model(model_id: int):
    """
    Endpoint to retrieve a single model by its ID.

    :param model_id: ID of the model to retrieve.
    :return: The model with the specified ID, or an error message if not found.
    """
    if model_id in models:
        return models[model_id]
    else:
        return {"Error": "Model not found"}

@app.patch("/models/update/{model_id}")
async def patch_model(model_id: int,
                      new_name: Annotated[str, Query(min_length=1, max_length=50)],
                      new_description: Annotated[str | None, Query(max_length=500)] = None
                      ):
    """
    Endpoint to update an existing model.

    :param model_id: ID of the model to modify.
    :param new_name: New name for the model.
    :param new_description: New description for the model.
    :return: The modified model, or an error message if not found.
    """
    if model_id in models:
        models[model_id] = Model(id = model_id, 
                                 name = new_name,
                                 description = new_description)
        return models[model_id]
    else:
        return {"Error": "Model not found"}
