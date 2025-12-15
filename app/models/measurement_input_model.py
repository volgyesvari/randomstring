from typing import Literal

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

class MeasurementInputModel(BaseModel):
    model_config = ConfigDict(frozen=True, alias_generator=to_camel)

    sensor_id: int
    metric_type: str = Literal["windSpeed", "humidity", "pressure", "temperature"]
    metric_value: float
    timestamp: int