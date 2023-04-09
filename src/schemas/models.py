"""
This module contains the pydantic models for the API.
"""

from pydantic import BaseModel, Field

class Model(BaseModel):
    id: int = Field(title="Model id")
    name: str = Field(title="Model name")
    description: str | None = Field(default=None, max_length=500,
                                    title="Model description")
    
    class Config:
        schema_extra = {
            "example" : {
                "id" : 11,
                "name" : "Model example",
                "description" : "Usefull model",
            }
        }
