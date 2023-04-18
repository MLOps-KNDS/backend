from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from models.base_class import Base
from sqlalchemy.orm import relationship

import enum


class Role(enum.Enum):
    OWNER = "owner"
    ADMIN = "admin"
    READER = "reader"
    WRITER = "writer"


class User(Base):
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)


class ModelUserRole(Base):
    id = Column(Integer, primary_key=True, unique=True)
    model_id = Column(Integer, ForeignKey("model.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    role = Column(Enum(Role), nullable=False)

    model = relationship("Model", backref="model_user_role")
    user = relationship("User", backref="model_user_role")


class PoolUserRole(Base):
    id = Column(Integer, primary_key=True, unique=True)
    pool_id = Column(Integer, ForeignKey("pool.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    role = Column(Enum(Role), nullable=False)

    pool = relationship("Pool", backref="pool_user_role")
    user = relationship("User", backref="pool_user_role")


class TestUserRole(Base):
    id = Column(Integer, primary_key=True, unique=True)
    test_id = Column(Integer, ForeignKey("test.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    role = Column(Enum(Role), nullable=False)

    test = relationship("Test", backref="test_user_role")
    user = relationship("User", backref="test_user_role")
