from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base_class import Base


class Test(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)
    created_by = Column(Integer, ForeignKey("user.id"))
    updated_at = Column(DateTime, nullable=False)
    updated_by = Column(Integer, ForeignKey("user.id"))

    creator = relationship(
        "User", foreign_keys="Test.created_by", back_populates="created_tests"
    )
    updater = relationship(
        "User", foreign_keys="Test.updated_by", back_populates="updated_tests"
    )

    models = relationship("ModelTest", back_populates="test")

    users_roles = relationship("TestUserRole", back_populates="test")
