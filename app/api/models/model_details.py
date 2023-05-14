from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from models.base_class import Base


class ModelDetails(Base):
    id = Column(
        Integer, ForeignKey("Model.id"), primary_key=True, autoincrement="ignore_fk"
    )
    artifact_uri = Column(String(255), nullable=False)
    image_tag = Column(String(255))
    replicas = Column(Integer, nullable=False)
    cpu_request = Column(String(255), nullable=False)
    cpu_limit = Column(String(255), nullable=False)
    memory_request = Column(String(255), nullable=False)
    memory_limit = Column(String(255), nullable=False)
    