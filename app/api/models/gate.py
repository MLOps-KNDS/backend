from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from models import Base


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

    users = relationship("GateUserRole", back_populates="gate")


class GatePool(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    gate_id = Column(Integer, ForeignKey("gate.id"), primary_key=True)
    pool_id = Column(Integer, ForeignKey("pool.id"), primary_key=True)

    gate = relationship("Gate", back_populates="pools")
    pool = relationship("Pool", back_populates="gates")


class GateUserRole(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    gate_id = Column(Integer, ForeignKey("gate.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)

    gate = relationship("Gate", back_populates="users")
    user = relationship("User", back_populates="gates")
