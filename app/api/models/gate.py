from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from models.base_class import Base
from models.user import Role


class Gate(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)
    created_by = Column(Integer, ForeignKey("user.id"), nullable=False)
    updated_at = Column(DateTime, nullable=False)
    updated_by = Column(Integer, ForeignKey("user.id"), nullable=False)

    creator = relationship(
        "User", foreign_keys="Gate.created_by", backref="created_gates"
    )
    updater = relationship(
        "User", foreign_keys="Gate.updated_by", backref="updated_gates"
    )

    pools = relationship("GatePool", back_populates="gate")

    users_roles = relationship("GateUserRole", back_populates="gate")


class GatePool(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    gate_id = Column(Integer, ForeignKey("gate.id"))
    pool_id = Column(Integer, ForeignKey("pool.id"))

    gate = relationship("Gate", back_populates="pools")
    pool = relationship("Pool", back_populates="gates")


class GateUserRole(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    gate_id = Column(Integer, ForeignKey("gate.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    role = Column(Enum(Role), nullable=False)

    gate = relationship("Gate", back_populates="users_roles")
    user = relationship("User", back_populates="gates")
