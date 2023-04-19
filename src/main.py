"""
This is the main module.

It contains the FastAPI app.
"""

from fastapi import FastAPI
from routers import models


app = FastAPI(title="Backend", description="MLOps", version="0.1.0")


app.include_router(models.router)


@app.get("/")
async def root() -> dict:
    """
    Root endpoint. Returns a simple message for testing purposes.

    :return: A "Server ON" message.
    """
    return {"Server": "ON"}
