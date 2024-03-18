"""Module for permission model"""

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from extensions.sql_session import Base


class Permission(Base):
    """Permission base"""
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True)
    email = Column(String(200), nullable=False)
    watch = Column(Boolean, nullable=False)
    approve = Column(Boolean, nullable=False)
    publish = Column(Boolean, nullable=False)

    # many to one
    fundId = Column("fundId", Integer,
                    ForeignKey("funds.id"), nullable=False)
    fund = relationship("Fund", back_populates="permissions")
