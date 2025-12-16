from datetime import datetime
from pydantic.dataclasses import dataclass
from pydantic import ConfigDict
from sqlalchemy.ext.asyncio import async_sessionmaker


from app.models.database_models import MetricItem
from app.models.measurement_input_model import MeasurementInputModel


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class MeasurementFacade:
    async_session_maker: async_sessionmaker

    async def create_item(self, event: MeasurementInputModel) -> MetricItem:
        item = MetricItem(**event.model_dump() | {'created_at': datetime.fromtimestamp(event.timestamp)})
        async with self.async_session_maker() as session:
            async with session.begin():  # Transaction starts here
                session.add(item)

        return item