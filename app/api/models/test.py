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

    # Test has .creator to access User. User has .created_tests to access list of all created tests
    creator = relationship("User", foreign_keys=created_by, back_populates="created_tests")
    # Test has .updater to access User. User has .updated_tests to access list of all updated tests
    updater = relationship("User", foreign_keys=updated_by, back_populates="updated_tests")

    # Test has .models to access list of all models
    models = relationship("ModelTest", back_populates="test")

    users_roles = relationship("TestUserRole", back_populates="test")