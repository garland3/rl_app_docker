from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import BLOB, Float
from .database import Base


class Job_t(Base):
    __tablename__ = "job"

    id = Column(Integer, primary_key=True, index=True)
    # email = Column(String, unique=True, index=True)
    # hashed_password = Column(String)
    # is_active = Column(Boolean, default=True)
    finished = Column(Boolean, default=False)
    working_on_job = Column(Boolean, default=False)
    message = Column(String, default="")
    timestamp = Column(TIMESTAMP)
    config = relationship("RLConfig_t", back_populates="job")
    designstatus = relationship("DesignStatus_t", back_populates="job")


class RLConfig_t(Base):
    __tablename__ = "RLconfig"
    id = Column(Integer, primary_key=True, index=True)
    bcs = Column(String)
    rights = Column(String)
    lefts = Column(String)
    downs = Column(String)
    ups = Column(String)
    volfraction = Column(Float)
    uuid = Column(String)

    job_id = Column(Integer, ForeignKey("job.id"))
    job = relationship("Job_t", back_populates="config")


class DesignStatus_t(Base):
    """Contains intermediate and final design info"""
    __tablename__ = "DesignStatus"
    id = Column(Integer, primary_key=True, index=True)
    progress = Column(Integer)
    timestamp = Column(TIMESTAMP)
    job_id = Column(Integer, ForeignKey("job.id"))
    # result = Column(String, default="")
    result = Column(BLOB)
    job = relationship("Job_t", back_populates="designstatus")


class Alive_t(Base):
    __tablename__ = "Alive"
    id = Column(Integer, primary_key=True, index=True)
    time = Column(TIMESTAMP)
