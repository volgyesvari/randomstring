from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class MetricItem(Base):
    __tablename__ = "measurements"
    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer)
    metric_type = Column(String)
    metric_value = Column(Float)
    timestamp = Column(Integer)
    created_at = Column(DateTime)