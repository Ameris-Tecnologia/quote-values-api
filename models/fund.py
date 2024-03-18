"""Module for fund model"""

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from extensions.sql_session import Base


class Fund(Base):
    """Fund base"""
    __tablename__ = "funds"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    active = Column(Boolean, nullable=False)
    sender = Column(String(30), nullable=False)

    # one to many
    uploads = relationship("Upload", back_populates="fund")
    permissions = relationship("Permission", back_populates="fund")
