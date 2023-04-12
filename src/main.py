"""
This is the main module.

It contains the FastAPI app.
"""

from fastapi import FastAPI


app = FastAPI(
    title="Backend Service",
    description="Backend Service for the ML Platform",
    version="0.1.0",
)


@app.get("/")
async def root() -> dict:
    """
    Root endpoint. Returns a simple message for testing purposes.

    :return: A "Hello World" message.
    """
    return {"message": "Hello World"}
