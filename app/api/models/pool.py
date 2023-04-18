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

    # Pool has .creator to access User. User has .created_pools to access list of all created pools
    creator = relationship("User", foreign_keys=created_by, backref="created_pools")
    # Pool has .updater to access User. User has .updated_pools to access list of all updated pools
    updater = relationship("User", foreign_keys=updated_by, backref="updated_pools")

    # Pool has .models to access list of all models
    models = relationship("ModelTest", back_populates="pool")

    users_roles = relationship("PoolUserRole", back_populates="pool")

class PoolModel(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    pool_id = Column(Integer, ForeignKey("pool.id"), primary_key=True)
    model_id = Column(Integer, ForeignKey("model.id"), primary_key=True)
    mode = Column(Enum(PoolModelModeEnum), nullable=False)

    # PoolModel has .model to access model. Model has .pools
    model = relationship("Model", back_populates="pools")
    # PoolModel has .pool to access pool. Pool has .models
    pool = relationship("Pool", back_populates="models")
