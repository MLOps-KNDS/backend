from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from models.base_class import Base


class ModelDetails(Base):
    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey("model.id"))
    artifact_uri = Column(String(255))
    image_tag = Column(String(255))
    replicas = Column(Integer)
    cpu_request = Column(String(255))
    cpu_limit = Column(String(255))
    memory_request = Column(String(255))
    memory_limit = Column(String(255))

    model = relationship(
        "Model",
        foreign_keys="ModelDetails.model_id",
        back_populates="model_details",
        uselist=False,
    )
