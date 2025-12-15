from datetime import datetime
from pydantic.dataclasses import dataclass
from pydantic import ConfigDict
from sqlalchemy import Engine
from sqlalchemy.orm import Session


from app.models.database_models import MetricItem
from app.models.measurement_input_model import MeasurementInputModel


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class MeasurementFacade:
    engine: Engine

    def create_item(self, event: MeasurementInputModel):
        item = MetricItem(**event.model_dump() | {'created_at': datetime.fromtimestamp(event.timestamp)})
        with Session(self.engine) as session:
            session.add(item)
            session.commit()
        return item