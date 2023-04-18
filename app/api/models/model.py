from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.base_class import Base
import enum


class Status(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Model(Base):
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)
    created_by = Column(Integer, ForeignKey("user.id"), primary_key=True)
    updated_at = Column(DateTime, nullable=False)
    updated_by = Column(Integer, ForeignKey("user.id"), primary_key=True)
    image_tag = Column(String(255))
    source_path = Column(String(255))
    status = Column(Enum(Status), nullable=False)

    creator = relationship("User", back_populates="created_models")
    updater = relationship("User", back_populates="updated_models")


class ModelTest(Base):
    id = Column(Integer, primary_key=True, unique=True)
    model_id = Column(Integer, ForeignKey("model.id"), primary_key=True)
    test_id = Column(Integer, ForeignKey("test.id"), primary_key=True)

    model = relationship("Model", back_populates="model_test")
    test = relationship("Test", back_populates="model_test")
