from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from base_class import Base

class RoleEnum(Enum):
    owner = "owner"
    admin = "admin"
    reader = "reader"
    writer = "writer"


class User(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)


class ModelUserRole(Base):
    model_id = Column(Integer, ForeignKey("model.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    role = Column(Enum(RoleEnum), nullable=False)
    model = relationship("Model", backref="user_roles")
    user = relationship("User", backref="model_roles")


class TestUserRole(Base):
    test_id = Column(Integer, ForeignKey("test.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    role = Column(Enum(RoleEnum), nullable=False)
    test = relationship("Test", backref="user_roles")
    user = relationship("User", backref="test_roles")


class PoolUserRole(Base):
    pool_id = Column(Integer, ForeignKey("pool.id"), primary_key=True)
