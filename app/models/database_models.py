from xmlrpc.client import DateTime

from sqlmodel import SQLModel, Field

from sqlalchemy import create_engine, Column, Integer, Float, select, func, String, DateTime
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()


class MetricItem(Base):
    __tablename__ = "measurements"
    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer)
    metric_type = Column(String)
    metric_value = Column(Float)
    timestamp = Column(Integer)
    created_at = Column(DateTime)