"""Module for user model"""

from sqlalchemy import Column, Integer, Text
from extensions.sql_session import Base


class User(Base):
    """User base"""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=True)
