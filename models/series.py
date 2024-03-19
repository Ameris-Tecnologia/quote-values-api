"""Module for series model"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL, BigInteger, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from extensions.sql_session import Base


class Series(Base):
    """Series base"""
    __tablename__ = "series"
    id = Column(Integer, primary_key=True)
    name = Column("name", String(30), nullable=False)
    bookValue = Column("bookValue", DECIMAL(
        asdecimal=False), nullable=False)
    economicValue = Column(
        "economicValue", DECIMAL(asdecimal=False), nullable=False
    )
    contributors = Column("contributors", Integer, nullable=False)
    institutionalContributors = Column(
        "institutionalContributors", Integer, nullable=False
    )
    issuedQuotes = Column(
        "issuedQuotes", DECIMAL(asdecimal=False), nullable=False
    )
    paidQuotes = Column("paidQuotes", DECIMAL(
        asdecimal=False), nullable=False)
    netEquity = Column("netEquity", DECIMAL(
        asdecimal=False), nullable=False)
    totalAssets = Column("totalAssets", BigInteger, nullable=False)
    pxqEquity = Column("pxqEquity", BigInteger, nullable=False)
    dataOk = Column("dataOk", Boolean, default=False)
    # pylint: disable=not-callable
    createdAt = Column("createdAt", DateTime, default=func.now())
    updatedAt = Column(
        "updatedAt",
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )

    # many to one
    uploadId = Column("uploadId", Integer, ForeignKey("uploads.id"))
    upload = relationship(
        "Upload",
        back_populates="series",
        cascade="delete, delete-orphan",
        single_parent=True,
    )
