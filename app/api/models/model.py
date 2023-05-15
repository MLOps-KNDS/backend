from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import enum

from models.base_class import Base


class Status(str, enum.Enum):
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
    status = Column(Enum(Status), nullable=False)
    # model_details_id = Column(Integer, ForeignKey("model_details.id"))

    creator = relationship(
        "User", foreign_keys="Model.created_by", back_populates="created_models"
    )
    updater = relationship(
        "User", foreign_keys="Model.updated_by", back_populates="updated_models"
    )

    tests = relationship("ModelTest", back_populates="model")

    pools = relationship("PoolModel", back_populates="model")

    users_roles = relationship("ModelUserRole", back_populates="model")

    model_details = relationship("ModelDetails", back_populates="model", uselist=False)


class ModelTest(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(Integer, ForeignKey("model.id"))
    test_id = Column(Integer, ForeignKey("test.id"))

    model = relationship("Model", back_populates="tests")

    test = relationship("Test", back_populates="models")
