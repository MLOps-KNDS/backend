"""
This file contains the Model class.
"""

from pydantic import BaseModel

class Model(BaseModel):
    id: int
    name: str