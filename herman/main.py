from fastapi import FastAPI, Path, Query
from fastapi.responses import JSONResponse
from typing import Annotated, Union, Dict
from pydantic import BaseModel, Field

app = FastAPI()


class ModelOut(BaseModel):
    model_id: int = Field(example=123)
    name: str = Field(example="Foo")
    description: Union[str, None] = Field(default=None, example="Description of Foo")

    class Config:
        schema_extra = {
            "example_with_desc": {
                "model_id": 123,
                "name": "Foo",
                "description": "A very nice Item",
            },
            "example_without_desc": {
                "model_id": 123,
                "name": "Foo",
            },
        }


class Message(BaseModel):
    message: str


models: list[ModelOut] = [
    ModelOut(model_id=1, name="Filip"),
    ModelOut(model_id=2, name="Mateusz", description="Jakis opis"),
    ModelOut(model_id=3, name="Seba", description="Jakis inny opis"),
    ModelOut(model_id=4, name="Mati"),
    ModelOut(model_id=5, name="Filip"),
    ModelOut(model_id=6, name="Mateusz", description="Jakis opis"),
    ModelOut(model_id=7, name="Seba", description="Jakis inny opis"),
    ModelOut(model_id=8, name="Mati"),
    ModelOut(model_id=9, name="Filip"),
    ModelOut(model_id=10, name="Mateusz", description="Jakis opis"),
    ModelOut(model_id=11, name="Seba", description="Jakis inny opis"),
    ModelOut(model_id=12, name="Mati"),
    ModelOut(model_id=13, name="Filip"),
    ModelOut(model_id=14, name="Mateusz", description="Jakis opis"),
    ModelOut(model_id=15, name="Seba", description="Jakis inny opis"),
    ModelOut(model_id=16, name="Mati"),
    ModelOut(model_id=17, name="Filip"),
    ModelOut(model_id=18, name="Mateusz", description="Jakis opis"),
    ModelOut(model_id=19, name="Seba", description="Jakis inny opis"),
    ModelOut(model_id=20, name="Mati"),
]


@app.get("/status/")
async def status():
    return {"status": "Working"}


@app.get("/api/models/", response_model=dict[int, ModelOut])
async def get_models(
    skip: Annotated[Union[int, None], Query(ge=0)] = None,
    limit: Annotated[Union[int, None], Query(ge=1)] = None,
):
    response: dict[int, ModelOut] = {}
    start = skip if skip else 0
    end = start + limit if limit else len(models)

    for index in range(start, end):
        try:
            response.update({index + 1: models[index]})
        except IndexError:
            break

    return response


@app.get(
    "/api/models/{id}/", response_model=ModelOut, responses={404: {"model": Message}}
)
async def get_by_id(id: Annotated[int, Path(title="Id of model you want to get")]):
    # Place for database implementation
    try:
        return models[id]
    except IndexError:
        return JSONResponse(status_code=404, content={"message": "Item not found"})


@app.patch(
    "/api/models/{id}/", response_model=ModelOut, responses={404: {"model": Message}}
)
async def patch_by_id(
    id: Annotated[int, Path(title="Id of model you want to get")],
    new_name: Annotated[Union[str, None], Query(max_length=50, min_length=3)] = None,
    new_desc: Annotated[Union[str, None], Query(max_length=50, min_length=3)] = None,
):
    # Place for database implementation
    try:
        if new_name:
            models[id].name = new_name
        if new_desc:
            models[id].description = new_desc
        return models[id]
    except IndexError:
        return JSONResponse(status_code=404, content={"message": "Item not found"})
