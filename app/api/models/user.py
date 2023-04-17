from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from models.base_class import Base
from sqlalchemy.orm import relationship

from enum import Enum as En


class RoleEnum(En):
    owner = "owner"
    admin = "admin"
    reader = "reader"
    writer = "writer"


class User(Base):
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)


class ModelUserRole(Base):
    id = Column(Integer, primary_key=True, unique=True)
    model_id = Column(Integer, ForeignKey("model.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    role = Column(Enum(RoleEnum), nullable=False)
    model = relationship("Model", backref="user_roles")
    user = relationship("User", backref="model_roles")


class PoolUserRole(Base):
    id = Column(Integer, primary_key=True, unique=True)
    pool_id = Column(Integer, ForeignKey("pool.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    role = Column(Enum(RoleEnum), nullable=False)
    pool = relationship("Pool", backref="pool_roles")
    user = relationship("User", backref="pool_users")


class TestUserRole(Base):
    id = Column(Integer, primary_key=True, unique=True)
    test_id = Column(Integer, ForeignKey("test.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    role = Column(Enum(RoleEnum), nullable=False)
    test = relationship("Test", backref="user_roles")
    user = relationship("User", backref="test_roles")
