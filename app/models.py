from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Experiment(Base):
    __tablename__ = "experiments"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False, index=True)
    hypothesis = Column(String)
    metric = Column(String, default="conversion")
    baseline_rate = Column(Float, default=0.10)
    mde = Column(Float, default=0.05)
    status = Column(String, default="running")
    created_at = Column(DateTime, server_default=func.now())
    observations = relationship("Observation", back_populates="experiment",
                                cascade="all, delete-orphan")

class Observation(Base):
    __tablename__ = "observations"
    id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    variant = Column(String, index=True)
    users = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    revenue = Column(Float, default=0.0)
    day = Column(Integer, default=0)
    experiment = relationship("Experiment", back_populates="observations")
