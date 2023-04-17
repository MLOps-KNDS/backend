from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from base_class import Base

from enum import Enum as En


class PoolModelModeEnum(En):
    PRODUCTION = "production"
    STAGING = "staging"


class Pool(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)
    created_by = Column(Integer, ForeignKey("user.id"), primary_key=True)
    updated_at = Column(DateTime, nullable=False)
    updated_by = Column(Integer, ForeignKey("user.id"), primary_key=True)
    creator = relationship("Creator", backref="created_pools")
    updater = relationship("Updater", backref="updated_pools")


class PoolModel(Base):
    id = Column(Integer, primary_key=True)
    pool_id = Column(Integer, ForeignKey("pool.id"), primary_key=True)
    model_id = Column(Integer, ForeignKey("model.id"), primary_key=True)
    mode = Column(Enum(PoolModelModeEnum), nullable=False)
    model = relationship("Model", backref="models")
    test = relationship("Test", backref="tests")
