"""
This is the main module.
It contains the FastAPI app.
"""

import time
from fastapi import FastAPI
from contextlib import asynccontextmanager
from starlette.middleware.sessions import SessionMiddleware
import logging
import secrets

from db.create import create_db
from utils.model_builder import ModelBuilder


from routers import (
    user,
    pool,
    gate,
    model,
    test,
    mlflow_server,
    login,
)

_logger = logging.getLogger(__name__)


@asynccontextmanager
async def init(app: FastAPI):
    time.sleep(5)
    # Create the database tables with initial data
    create_db()
    ModelBuilder.build_base_image()
    yield


app = FastAPI(
    title="Backend Service",
    description="Backend Service for the ML Platform",
    version="0.1.0",
    lifespan=init,
)

app.include_router(user.router)
app.include_router(pool.router)
app.include_router(gate.router)
app.include_router(model.router)
app.include_router(test.router)
app.include_router(mlflow_server.router)
app.include_router(login.router)

app.add_middleware(SessionMiddleware, secret_key=secrets.token_bytes(32))


@app.get("/")
async def root() -> dict:
    """
    Root endpoint. Returns a simple message for testing purposes.
    :return: A "Hello World" message.
    """
    return {"message": "Hello World"}
