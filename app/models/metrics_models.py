from datetime import datetime
from typing import Literal
from fastapi import Query

from pydantic import BaseModel, ConfigDict, field_validator, model_validator, Field
from pydantic.alias_generators import to_camel

class MetricsInputModel(BaseModel):
    model_config = ConfigDict(frozen=True, alias_generator=to_camel, populate_by_name=True)

    sensor_ids: list[int] = Field(Query(...))
    metrics: list[Literal["windSpeed", "humidity", "pressure", "temperature"]] = Field(Query(...))
    statistic: Literal["min", "max", "sum", "average"] = Field(Query(...))
    start_date: datetime = Field(Query(...))
    end_date: datetime = Field(Query(...))

    @model_validator(mode="after")
    def validate_date_range(self):
        if not 1 <= (self.end_date - self.start_date).days <= 30:
            raise ValueError("Invalid date range")

    @field_validator("metrics",mode="before")
    @classmethod
    def validate_metrics(cls, v):
        v = set(v)
        v = list(v)
        v.sort()
        return v


class MetricModel(BaseModel):
    model_config = ConfigDict(frozen=True, alias_generator=to_camel, populate_by_name=True)

    sensor_id: int
    metric: Literal["windSpeed", "humidity", "pressure", "temperature"]
    statistic: Literal["min", "max", "sum", "average"]
    start_date: datetime
    end_date: datetime
    value: float
