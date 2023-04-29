"""
This is the main module.
It contains the FastAPI app.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager
import time

from db.create import create_db
from db.session import engine

from routers import (
    user,
    pool,
    model,
    test,
)


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

app.include_router(model.router)
app.include_router(user.router)
app.include_router(pool.router)
app.include_router(test.router)


@app.get("/")
async def root() -> dict:
    """
    Root endpoint. Returns a simple message for testing purposes.
    :return: A "Hello World" message.
    """
    return {"message": "Hello World"}
