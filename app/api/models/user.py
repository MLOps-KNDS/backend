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
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)

    created_models = relationship("Model", back_populates="creator")
    updated_models = relationship("Model", back_populates="updater")

    created_tests = relationship("Test", back_populates="creator")
    updated_tests = relationship("Test", back_populates="updater")

    models_roles = relationship("ModelUserRole", back_populates="user")

    pools_roles = relationship("PoolUserRole", back_populates="user")

    tests_roles = relationship("TestUserRole", back_populates="user")

class ModelUserRole(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(Integer, ForeignKey("model.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    role = Column(Enum(Role), nullable=False)


    model = relationship("Model", back_populates="users_role")
    user = relationship("User", back_populates="models_role")


class PoolUserRole(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    pool_id = Column(Integer, ForeignKey("pool.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    role = Column(Enum(Role), nullable=False)

    pool = relationship("Pool", backref="users_roles")
    user = relationship("User", backref="pools_roles")


class TestUserRole(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    test_id = Column(Integer, ForeignKey("test.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    role = Column(Enum(Role), nullable=False)

    test = relationship("Test", backref="users_roles")
    user = relationship("User", backref="tests_roles")
