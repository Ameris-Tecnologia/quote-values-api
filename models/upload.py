"""Module for upload model"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from extensions.sql_session import Base


class Upload(Base):
    """Upload base"""
    __tablename__ = "uploads"
    id = Column(Integer, primary_key=True)
    date = Column("date", String(15), nullable=False)

    agency = Column("agency", String(50), nullable=False)
    currency = Column("currency", String(10), nullable=False)

    status = Column(
        "status", String(30),
        nullable=False,
        default="RECEIVED"
    )
    error = Column("error", String(200), default=None)
    approvedBy = Column(String(50))
    approvalMethod = Column(String(10))
    publishedBy = Column(String(50))

    s3Id = Column("s3Id", String(60))
    traceId = Column("traceId", String(40), nullable=False)

    # pylint: disable=not-callable
    createdAt = Column("createdAt", DateTime, default=func.now())
    updatedAt = Column(
        "updatedAt",
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )

    # one to many
    series = relationship(
        "Series", back_populates="upload", cascade="delete")

    # many to one
    fundId = Column("fundId", Integer,
                    ForeignKey("funds.id"), nullable=False)
    fund = relationship("Fund", back_populates="uploads")
