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


from routers import (
    user,
    pool,
    gate,
    model,
    test,
    login,
)

_logger = logging.getLogger(__name__)


@asynccontextmanager
async def init(app: FastAPI):
    time.sleep(5)
    # Create the database tables with initial data
    create_db()
    yield


app = FastAPI(
    title="Backend Service",
    description="Backend Service for the ML Platform",
    version="0.1.0",
    lifespan=init,
    routes=[
        model.router,
        user.router,
        pool.router,
        gate.router,
        test.router,
        login.router,
    ],
)

app.add_middleware(SessionMiddleware, secret_key=secrets.token_bytes(32))


@app.get("/")
async def root() -> dict:
    """
    Root endpoint. Returns a simple message for testing purposes.
    :return: A "Hello World" message.
    """
    return {"message": "Hello World"}
