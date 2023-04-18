import enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

from models import Base


class PoolModelModeEnum(enum.Enum):
    PRODUCTION = "production"
    STAGING = "staging"


class Pool(Base):
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)
    created_by = Column(Integer, ForeignKey("user.id"), nullable=False)
    updated_at = Column(DateTime, nullable=False)
    updated_by = Column(Integer, ForeignKey("user.id"), nullable=False)

    creator = relationship("User", back_populates="created_pools")
    updater = relationship("User", back_populates="updated_pools")


class PoolModel(Base):
    id = Column(Integer, primary_key=True, unique=True)
    pool_id = Column(Integer, ForeignKey("pool.id"), primary_key=True)
    model_id = Column(Integer, ForeignKey("model.id"), primary_key=True)
    mode = Column(Enum(PoolModelModeEnum), nullable=False)

    pool = relationship("Pool", back_populates="pool_model")
    model = relationship("Model", back_populates="pool_model")
