"""
This file contains the Test model
"""

from pydantic import BaseModel


class Test(BaseModel):
    id: int
    name: str