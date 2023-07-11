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
    mlflow_server_id = Column(Integer, ForeignKey("mlflow_server.id"))
    artifact_uri = Column(String(255))
    image_tag = Column(String(255))
    min_replicas = Column(Integer)
    max_replicas = Column(Integer)
    cpu_request = Column(String(255))
    cpu_limit = Column(String(255))
    cpu_utilization = Column(Integer)
    memory_request = Column(String(255))
    memory_limit = Column(String(255))
    memory_utilization = Column(Integer)

    model = relationship(
        "Model",
        foreign_keys="ModelDetails.model_id",
        back_populates="model_details",
        uselist=False,
    )

    mlflow_server = relationship(
        "MlflowServer",
        foreign_keys="ModelDetails.mlflow_server_id",
        uselist=False,
    )
