from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from base_class import Base


class Test(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)
    created_by = Column(Integer, ForeignKey("user.id"), primary_key=True)
    updated_at = Column(DateTime, nullable=False)
    updated_by = Column(Integer, ForeignKey("user.id"), primary_key=True)
    creator = relationship("Creator", backref="created_tests")
    updater = relationship("Updater", backref="updated_tests")
