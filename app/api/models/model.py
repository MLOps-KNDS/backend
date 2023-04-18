from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.base_class import Base
import enum


class Status(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Model(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)
    created_by = Column(Integer, ForeignKey("user.id"))
    updated_at = Column(DateTime, nullable=False)
    updated_by = Column(Integer, ForeignKey("user.id"))
    image_tag = Column(String(255))
    source_path = Column(String(255))
    status = Column(Enum(Status), nullable=False)

    # Model has .creator to access User. User has .created_models to access list of all created models
    creator = relationship("User", foreign_keys=created_by, back_populates="created_models")
    # Model has .updater to access User. User has .updated_models to access list of all updated models
    updater = relationship("User", foreign_keys=updated_by, backref="updated_models")

    # Model has .tests to access list of all tests
    tests = relationship("ModelTest", back_populates="model")

    # Model has .pools to access list of all pools
    pools = relationship("PoolModel", back_populates="model")

    users_role = relationship("ModelUserRole", back_populates="model")


class ModelTest(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(Integer, ForeignKey("model.id"), primary_key=True)
    test_id = Column(Integer, ForeignKey("test.id"), primary_key=True)

    # ModelTest has .model to access model. Model has .tests
    model = relationship("Model", back_populates="tests")
    # ModelTest has .test to access model. Test has .models
    test = relationship("Test", back_populates="models")
