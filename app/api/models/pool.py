import enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

from models import Base


class PoolModelModeEnum(enum.Enum):
    PRODUCTION = "production"
    STAGING = "staging"


class Pool(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)
    created_by = Column(Integer, ForeignKey("user.id"), nullable=False)
    updated_at = Column(DateTime, nullable=False)
    updated_by = Column(Integer, ForeignKey("user.id"), nullable=False)

    creator = relationship(
        "User", foreign_keys="Pool.created_by", backref="created_pools"
    )
    updater = relationship(
        "User", foreign_keys="Pool.updated_by", backref="updated_pools"
    )

    models = relationship("PoolModel", back_populates="pool")

    users_roles = relationship("PoolUserRole", back_populates="pool")

    gates = relationship("GatePool", back_populates="pool")


class PoolModel(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    pool_id = Column(Integer, ForeignKey("pool.id"))
    model_id = Column(Integer, ForeignKey("model.id"))
    mode = Column(Enum(PoolModelModeEnum), nullable=False)
    weight = Column(Integer, nullable=False)

    model = relationship("Model", back_populates="pools")
    pool = relationship("Pool", back_populates="models")
