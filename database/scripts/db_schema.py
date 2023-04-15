from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, DeclarativeBase

from enum import Enum as En


class StatusEnum(En):
    active = "active"
    inactive = "inactive"


class RoleEnum(En):
    owner = "owner"
    admin = "admin"
    reader = "reader"
    writer = "writer"


class Base(DeclarativeBase):
    __allow_unmapped__ = True


class Model(Base):
    __tablename__ = "model"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)
    created_by = Column(Integer, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    updated_by = Column(Integer, nullable=False)
    image_tag = Column(String(255))
    source_path = Column(String(255))
    status: Column(Enum(StatusEnum), nullable=False)


class Test(Base):
    __tablename__ = "test"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)
    created_by = Column(Integer, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    updated_by = Column(Integer, nullable=False)


class ModelTest(Base):
    __tablename__ = "model_test"
    model_id = Column(Integer, ForeignKey("model.id"), primary_key=True)
    test_id = Column(Integer, ForeignKey("test.id"), primary_key=True)
    model = relationship("Model", backref="tests")
    test = relationship("Test", backref="models")


class Pool(Base):
    __tablename__ = "pool"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)
    created_by = Column(Integer, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    updated_by = Column(Integer, nullable=False)


class PoolModel(Base):
    __tablename__ = "pool_model"
    pool_id = Column(Integer, ForeignKey("pool.id"), primary_key=True)
    model_id = Column(Integer, ForeignKey("model.id"), primary_key=True)
    pool = relationship("Pool", backref="models")
    model = relationship("Model", backref="pools")


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)


class ModelUserRole(Base):
    __tablename__ = "model_user_role"
    model_id = Column(Integer, ForeignKey("model.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    role = Column(Enum(RoleEnum), nullable=False)
    model = relationship("Model", backref="user_roles")
    user = relationship("User", backref="model_roles")


class TestUserRole(Base):
    __tablename__ = "test_user_role"
    test_id = Column(Integer, ForeignKey("test.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    role = Column(Enum(RoleEnum), nullable=False)
    test = relationship("Test", backref="user_roles")
    user = relationship("User", backref="test_roles")


class PoolUserRole(Base):
    __tablename__ = "pool_user_role"
    pool_id = Column(Integer, ForeignKey("pool.id"), primary_key=True)
