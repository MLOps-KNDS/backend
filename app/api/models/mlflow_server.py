from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from models.base_class import Base


class MlflowServer(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    tracking_uri = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    created_by = Column(Integer, ForeignKey("user.id"))
    updated_at = Column(DateTime, nullable=False)
    updated_by = Column(Integer, ForeignKey("user.id"))

    creator = relationship("User", foreign_keys="MlflowServer.created_by", backref="created_mlflow_servers")
    updater = relationship("User", foreign_keys="MlflowServer.updated_by", backref="updated_mlflow_servers")
