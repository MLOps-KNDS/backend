"""
This is the main module.

It contains the FastAPI app.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager
import time

from db.create import create_db
from db.session import engine
from utils.image_builder import ImageBuilder


image_builder = ImageBuilder(
    name="test2",
    model_uri="/mnt/saved_model",
)
image_builder.build()


@asynccontextmanager
async def init(app: FastAPI):
    time.sleep(5)
    create_db(engine)
    yield


app = FastAPI(
    title="Backend Service",
    description="Backend Service for the ML Platform",
    version="0.1.0",
    lifespan=init,
)


@app.get("/")
async def root() -> dict:
    """
    Root endpoint. Returns a simple message for testing purposes.

    :return: A "Hello World" message.
    """
    return {"message": "Hello World"}
