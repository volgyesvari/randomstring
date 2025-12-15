from pydantic.dataclasses import dataclass
from pydantic import ConfigDict
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy import RowMapping, select, func, Sequence
from app.models.database_models import MetricItem
from app.models.metrics_models import MetricsInputModel


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class MetricsDAO:
    engine: Engine


    def get_metric(self, event: MetricsInputModel, metric: str) -> Sequence[RowMapping]:
        func_dict = {"min": func.min,
                     "max": func.max,
                     "sum": func.sum,
                     "average": func.avg}
        with Session(self.engine) as session:
            stmt = select(
                MetricItem.sensor_id.label("sensor_id"),
                MetricItem.metric_type.label("metric"),
                func_dict[event.statistic](MetricItem.metric_value).label("value"),
            ).where(
                MetricItem.sensor_id.in_(event.sensor_ids)
            ).where(MetricItem.created_at.between(event.start_date, event.end_date)
            ).where(MetricItem.metric_type == metric
            ).group_by(MetricItem.sensor_id
            ).group_by(MetricItem.metric_type)

            return session.execute(stmt).mappings().all()

