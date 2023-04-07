"""
This is the main module.

It contains the FastAPI app.
"""


from fastapi import FastAPI

app = FastAPI()

async def get_root() -> dict:
    """
    This is the root path.

    :return: A dict with a "Hello" key and a "World" value.
    """
    return {"Hello": "World"}

async def get_item(item_id: int):
    """
    This is the item path.

    :param item_id: The item id.
    :return: A dict with an "item_id" key and the item id value.
    """
    return {"item_id": item_id}