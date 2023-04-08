from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4


class MLModel(BaseModel):
    id: Optional[UUID] = uuid4()
    name: str
    description: str
    created_by: int
    updated_by: int
    image_tag: str
    source_path: str

    def update(self, update_data: dict) -> None:
        """
        Upadate one or more fields in model.

        :param update_data: Dictionary with changed fields.
        :type update_data: dict

        :return: All ML Models.
        :rtype: List[MLModel]
        """
        for key, value in update_data.items():
            if hasattr(self, key):
                setattr(self, key, value)
