from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import enum

from models.base_class import Base


class ModelStatus(str, enum.Enum):
    INACTIVE = "inactive"
    
    BUILT = "built"
    BUILDING = "building"
    BUILD_FAILED = "build_failed"

    PUSHED = "pushed"
    PUSHING = "pushing"
    PUSH_FAILED = "push_failed"

    DEPLOYED = "deployed"
    DEPLOYING = "deploying"
    DEPLOY_FAILED = "deploy_failed"

    DEACTIVATING = "deactivating"
    DEACTIVATION_FAILED = "deactivation_failed"


class Model(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)
    created_by = Column(Integer, ForeignKey("user.id"))
    updated_at = Column(DateTime, nullable=False)
    updated_by = Column(Integer, ForeignKey("user.id"))
    status = Column(Enum(ModelStatus), nullable=False)

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
