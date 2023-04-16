from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from base_class import Base

class PoolModelModeEnum(Enum):
    PRODUCTION = "production"
    STAGING = "staging"


class Pool(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)
    created_by = Column(Integer, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    updated_by = Column(Integer, nullable=False)


class PoolModel(Base):
    id = Column(Integer, primary_key=True)
    pool_id = Column(Integer, ForeignKey("pool.id"), primary_key=True)
    model_id = Column(Integer, ForeignKey("model.id"), primary_key=True)
    mode = Column(Enum(PoolModelModeEnum), nullable=False)
