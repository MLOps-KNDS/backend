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
    artifact_uri = Column(String(255), nullable=False)
    image_tag = Column(String(255))
    replicas = Column(Integer, nullable=False)
    cpu_request = Column(String(255), nullable=False)
    cpu_limit = Column(String(255), nullable=False)
    memory_request = Column(String(255), nullable=False)
    memory_limit = Column(String(255), nullable=False)

    model = relationship("Model", back_populates="model_details")
