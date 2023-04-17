from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from base_class import Base

from enum import Enum as En


class StatusEnum(En):
    active = "active"
    inactive = "inactive"


class Model(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)
    created_by = Column(Integer, ForeignKey("user.id"), primary_key=True)
    updated_at = Column(DateTime, nullable=False)
    updated_by = Column(Integer, ForeignKey("user.id"), primary_key=True)
    image_tag = Column(String(255))
    source_path = Column(String(255))
    status = Column(Enum(StatusEnum), nullable=False)
    creator = relationship("Creator", backref="created_models")
    updater = relationship("Updater", backref="created_models")


class ModelTest(Base):
    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey("model.id"), primary_key=True)
    test_id = Column(Integer, ForeignKey("test.id"), primary_key=True)
    model = relationship("Model", backref="models")
    test = relationship("Test", backref="tests")
