from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from models.base_class import Base
from sqlalchemy.orm import relationship

import enum


class UserRole(enum.Enum):
    OWNER = "owner"
    ADMIN = "admin"
    READER = "reader"
    WRITER = "writer"


class User(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)

    created_models = relationship(
        "Model", foreign_keys="Model.created_by", back_populates="creator"
    )
    updated_models = relationship(
        "Model", foreign_keys="Model.updated_by", back_populates="updater"
    )

    created_tests = relationship(
        "Test", foreign_keys="Test.created_by", back_populates="creator"
    )
    updated_tests = relationship(
        "Test", foreign_keys="Test.updated_by", back_populates="updater"
    )

    models_roles = relationship("ModelUserRole", back_populates="user")

    pools_roles = relationship("PoolUserRole", back_populates="user")

    tests_roles = relationship("TestUserRole", back_populates="user")

    gates = relationship("GateUserRole", back_populates="user")


class ModelUserRole(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(Integer, ForeignKey("model.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    role = Column(Enum(UserRole), nullable=False)

    model = relationship("Model", back_populates="users_roles")
    user = relationship("User", back_populates="models_roles")


class PoolUserRole(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    pool_id = Column(Integer, ForeignKey("pool.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    role = Column(Enum(UserRole), nullable=False)

    pool = relationship("Pool", back_populates="users_roles")
    user = relationship("User", back_populates="pools_roles")


class TestUserRole(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    test_id = Column(Integer, ForeignKey("test.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    role = Column(Enum(UserRole), nullable=False)

    test = relationship("Test", back_populates="users_roles")
    user = relationship("User", back_populates="tests_roles")
